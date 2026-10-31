# Architecture et contrats

## Construction directe

`ToastBuilder` encapsule une référence `Microsoft.Toolkit.Uwp.Notifications.ToastContentBuilder`. Les méthodes publiques modifient immédiatement cet objet .NET ; aucune description intermédiaire LabVIEW n'est stockée. L'ancienne classe LabVIEW `ToastContent` a été retirée. Le type .NET homonyme reste un détail interne de la sérialisation.

Les nœuds de propriétés de classe donnent accès aux références stockées. Les dossiers virtuels Public, Community, Protected et Private décrivent les scopes ; les dossiers physiques sont plats, un par classe ou bibliothèque. Les accesseurs restent regroupés dans les propriétés natives.

## Responsabilités

| Composant | Rôle |
|---|---|
| ToastBuilder | Create, Add Text, Add Text Input, Add Bouton, Get XML, Show, Close |
| ToastService | Initialize, Register For Events avec handler injecté, Show sur un builder emprunté, Close |
| ActivationHandler.Handle Activation | Extension à dispatch dynamique ; le gestionnaire de base affiche actuellement les données en JSON |
| Toast Native.lvlib | Appels directs du toolkit, construction et manipulation des objets natifs |
| Reflection DotNet.lvlib | Métadonnées de réflexion, lecture de propriétés, invocation d'interface et fermeture des handles |
| Activation.ctl / Argument.ctl | Arguments d'activation bruts et tableau de paires Key/Value copiés en LabVIEW |

`Initialize` prépare la référence du gestionnaire natif. Le handler est injecté séparément dans `Register For Events`, comme paramètre utilisateur du callback `OnActivated`.
Les arguments restent une chaîne brute : aucun format de parsing n'est imposé à tous les gestionnaires.

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
| Queue ou événement utilisateur d'un handler applicatif | Appelant | Après arrêt de ses utilisateurs |

Une copie de classe ne rend pas les handles indépendants. Fermer un alias invalide les autres. `reference out` et `object out` désignent des alias empruntés ; ils ne doivent pas être fermés comme des acquisitions supplémentaires.
Fermer un handle LabVIEW, appeler `Dispose`, désabonner un événement et déclencher le GC sont des opérations distinctes.

Les opérations ignorées sur erreur entrante utilisent des cases Error/No Error. Les helpers de nettoyage travaillent aussi avec une erreur entrante et placent l'erreur principale en premier lors de la fusion. Le callback transmet l'erreur de conversion à `Handle Activation` ; `Last Callback Error` expose son erreur de sortie. Le payload ne contient plus de champ Error.

## Fermeture et limites

L'exemple attend Stop avant de fermer le service, puis le builder, et de déclencher une collecte .NET ponctuelle pour libérer le callback réservé observé sur le poste.
Le handler doit retourner rapidement, déléguer le travail long et ne jamais attendre le thread qui ferme le service ni appeler lui-même cette fermeture. Les modifications d'une copie du handler ne constituent pas un état partagé : utiliser des références explicites de communication si nécessaire.

Le protocole complet restant devra empêcher les nouveaux envois pendant Closing, désabonner, attendre de façon bornée les callbacks engagés, conserver leurs ressources en cas de timeout, puis passer en Closed. Le rollback d'acquisitions partielles, les doubles enregistrements et les fermetures répétées du service restent à durcir.
La gestion de tous les temporaires de composition reste également à revoir, notamment le handle du bouton créé par Add Bouton. Ne pas interpréter la première phase comme une preuve d'absence de fuite ou de sûreté concurrente.

## Passages de relais

Enregistrer les VIs avant de changer de main. Ne pas modifier simultanément les mêmes fichiers dans l'IDE et par les outils.
Les VIs enregistrés sont la source de vérité. Les intermédiaires sous `_review` ne doivent pas servir à régénérer les VIs remaniés manuellement.
