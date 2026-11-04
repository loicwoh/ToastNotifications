# Architecture — notes de maintenance

> Point d’entrée utilisateur : [API par propriétaire](docs/site/api.md) et
> [contrat courant de callback/ownership](docs/site/callbacks.md). Ce document
> conserve des notes d’implémentation pour les mainteneurs ; les guides publics
> et leurs sources canoniques sont décrits dans [CONTENT-MAP](docs/CONTENT-MAP.md).

## Construction directe

`ToastBuilder` encapsule une référence `Microsoft.Toolkit.Uwp.Notifications.ToastContentBuilder`. Les méthodes publiques modifient immédiatement cet objet .NET ; aucune description intermédiaire LabVIEW n'est stockée. L'ancienne classe LabVIEW `ToastContent` a été retirée. Le type .NET homonyme reste un détail interne de la sérialisation.

Les nœuds de propriétés de classe donnent accès aux références stockées. Les dossiers virtuels Public, Community, Protected et Private décrivent les scopes ; les dossiers physiques sont plats, un par classe ou bibliothèque. Les accesseurs restent regroupés dans les propriétés natives.

## Responsabilités

| Composant | Rôle |
|---|---|
| ToastSource | Classe mère : Show, Get XML et Close à dispatch dynamique ; les méthodes de base ne font pas de travail natif |
| Create ToastSource (Poly) | Sélection du constructeur concret : Create ToastBuilder ou Create ToastFromXML |
| ToastFromXML | Source XML : constructeur depuis une chaîne, document WinRT privé, Get XML, Show et Close ; le constructeur doit encore durcir le nettoyage sur échec de chargement |
| ToastBuilder | Implémentation de ToastSource : Create ToastBuilder, Add Text, Add Text Input, Add Bouton, Add Link Button, Set Activation Arguments, Get XML, Show, Close |
| ToastService | Initialize avec handler injecté, Register For Events, Show sur une ToastSource empruntée, sans cast vers ToastBuilder, Close |
| ActivationHandler.Handle Activation | Extension à dispatch dynamique ; le gestionnaire de base ne fait aucune action applicative |
| ActivationHandler.Initialize / Close | Hooks de cycle de vie pilotés par ToastService |
| UserEventActivationHandler | Crée un User Event, relaie Activation et l'erreur de conversion, puis détruit l'événement à sa fermeture |
| Toast Native.lvlib | Appels directs du toolkit, construction et manipulation des objets natifs |
| Reflection DotNet.lvlib | Métadonnées de réflexion, lecture de propriétés, invocation d'interface et fermeture des handles |
| Activation.ctl / Argument.ctl | Arguments d'activation bruts et tableau de paires Key/Value copiés en LabVIEW |

`ToastService.Initialize` reçoit le handler, prépare la référence native et appelle `Handler.Initialize`. Il conserve l'instance retournée, également exposée en sortie pour que l'appelant récupère ses références de communication. `Register For Events` transmet le handler stocké au callback `OnActivated`. `Close` appelle le hook de fermeture du handler ; l'attente des callbacks engagés reste à durcir.
Les arguments restent une chaîne brute : aucun format de parsing n'est imposé à tous les gestionnaires.

`Add Link Button` appelle directement `ToastContentBuilder.AddButton(content, activationType, arguments)` avec `activationType = Protocol` et la chaîne `URl` sur `arguments`. Il n'acquiert ni `System.Uri` ni handle `ToastButton` séparé. Windows ouvre l'URI à l'activation du bouton ; le handler LabVIEW n'est pas appelé pour cette action. Le corps du toast conserve son activation applicative distincte, sans réaction visible avec le handler de base actuel. La validation des URI reste déléguée au toolkit et à Windows.

## Propriété et erreurs

| Ressource | Propriétaire | Fin de vie |
|---|---|---|
| Handle du builder | Appelant qui possède ToastBuilder | ToastBuilder.Close |
| Référence de contenu lue par Get XML | Méthode de sérialisation | Après lecture |
| Référence native et abonnement du service | ToastService | Désenregistrement, puis fermeture du handle |
| Event Data.e et Control Ref | Mécanisme de callback | Empruntés ; aucune fermeture dans le convertisseur |
| Type, PropertyInfo, MethodInfo et résultats boxés acquis | Helper ou appelant indiqué par son contrat | Après consommation, y compris sur les chemins d'erreur |
| Énumérateur UserInput | Helper d'énumération | Dispose si disponible, puis Close Reference |
| Payload Activation | Valeurs LabVIEW | Durée de vie automatique |
| User Event de UserEventActivationHandler | Handler | Son hook Close ; les callbacks engagés doivent avoir cessé de l'utiliser |
| Event Registration Ref de la boucle applicative | Appelant | Unregister For Events après la réception, selon le protocole d'arrêt |
| Autres références d'un handler personnalisé | Selon son contrat explicite | Après arrêt de leurs utilisateurs |

Une copie de classe ne rend pas les handles indépendants. Fermer un alias invalide les autres. `reference out` et `object out` désignent des alias empruntés ; ils ne doivent pas être fermés comme des acquisitions supplémentaires.
Fermer un handle LabVIEW, appeler `Dispose`, désabonner un événement et déclencher le GC sont des opérations distinctes.

Les opérations ignorées sur erreur entrante utilisent des cases Error/No Error. Les helpers de nettoyage travaillent aussi avec une erreur entrante et placent l'erreur principale en premier lors de la fusion. Le callback transmet l'erreur de conversion séparément à `Handle Activation`. Le handler User Event la transporte à côté d'Activation dans son payload de livraison ; Activation.ctl ne contient pas ce champ. Aucun accesseur `Last Callback Error` n'est présent dans la classe actuelle ; consulter le contrat courant pour les diagnostics disponibles et les limites de #22.

## Fermeture et limites

Le wrapper de livraison `Activation Event Data.ctl` du handler User Event ajoute le champ `error` à côté d'`Activation` pour transporter l'erreur de conversion. Le typedef `Activation.ctl` reste inchangé. L'erreur de génération de l'événement n'est pas encore exposée par ce handler ; cette limite reste suivie dans #22. Voir `Examples/Multiple Actions.md`.

L'exemple attend Stop avant de fermer le service, puis le builder, et de déclencher une collecte .NET ponctuelle pour libérer le callback réservé observé sur le poste.
Le handler doit retourner rapidement, déléguer le travail long et ne jamais attendre le thread qui ferme le service ni appeler lui-même cette fermeture. Les modifications d'une copie du handler ne constituent pas un état partagé : utiliser des références explicites de communication si nécessaire.

Le protocole complet restant devra empêcher les nouveaux envois pendant Closing, désabonner, attendre de façon bornée les callbacks engagés, conserver leurs ressources en cas de timeout, puis passer en Closed. Le rollback d'acquisitions partielles, les doubles enregistrements et les fermetures répétées du service restent à durcir.
La gestion de tous les temporaires de composition reste également à revoir, notamment le handle du bouton créé par Add Bouton. Ne pas interpréter la première phase comme une preuve d'absence de fuite ou de sûreté concurrente.

## Passages de relais

Enregistrer les VIs avant de changer de main. Ne pas modifier simultanément les mêmes fichiers dans l'IDE et par les outils.
Les VIs enregistrés sont la source de vérité. Les intermédiaires sous `_review` ne doivent pas servir à régénérer les VIs remaniés manuellement.
