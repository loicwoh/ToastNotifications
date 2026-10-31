# Architecture et contrats

## Construction directe

`ToastBuilder` possède une référence privée `Microsoft.Toolkit.Uwp.Notifications.ToastContentBuilder`.
Les opérations modifient immédiatement cet objet .NET, sans moteur de conversion d'une description LabVIEW.
L'ancienne classe LabVIEW `ToastContent` a été retirée. Le type .NET homonyme du toolkit reste un détail interne.

Les accesseurs natifs de la référence sont privés. Les méthodes métier les utilisent via des nœuds de propriétés.
Les classes sont rangées dans les dossiers virtuels Public, Community, Protected et Private ; les propriétés restent regroupées.

## Méthodes actuelles

| Classe | Méthode | Comportement |
| --- | --- | --- |
| ToastBuilder | Create | Libère l'ancien handle puis crée un builder ; ignore l'opération sur erreur entrante |
| ToastBuilder | Add Text | Appelle immédiatement AddText ; conserve l'objet sur erreur entrante |
| ToastBuilder | Get XML | Lit le XML et ferme la référence temporaire de contenu |
| ToastBuilder | Show | Déclenche l'appel natif Show sans fermer le builder |
| ToastBuilder | Close | Ferme un handle valide même sur erreur entrante ; fermetures répétées acceptées |
| ToastService | Initialize | Retourne un service par défaut ; Handler accepté mais non conservé, aucun abonnement |
| ToastService | Show | Emprunte un ToastBuilder et délègue à son Show ; service et erreur transmis |
| ToastService | Close | Actuellement aucune ressource détenue : service et erreur transmis |
| ActivationHandler | Handle Activation | Surcharge dynamique ; méthode de base : erreur 7621 |

Les opérations de construction et d'affichage sont statiques. Seul le traitement du gestionnaire utilise le dispatch dynamique.
Pattern de connecteur 4815 : classe entrée 11, classe sortie 3, erreur entrée 8, erreur sortie 0.
Les paramètres additionnels et sorties, tels que le builder emprunté par le service et le XML, occupent les autres connecteurs.
Le service ne retourne pas actuellement le builder ; le fil d'erreur ordonne sa fermeture après Show.

## Propriété des ressources

| Ressource | Propriétaire | Fin de vie |
| --- | --- | --- |
| Handle natif du builder | Appelant qui possède ToastBuilder | Close, ou réinitialisation par Create |
| Handle temporaire de contenu lu par Get XML | Get XML | Après lecture, sur le chemin de nettoyage |
| Références créées par les VIs natifs utilisés directement | Appelant de ces VIs | Fermeture explicite après leur dernière utilisation |
| Payload Activation et paires Argument | Valeurs LabVIEW | Durée de vie automatique |
| Futur abonnement et contexte de callback | ToastService | Désabonnement, attente des callbacks engagés, puis libération |
| Futures références de réflexion Type/PropertyInfo/MethodInfo | Méthode qui les acquiert | Après utilisation, y compris sur erreur |
| Futurs énumérateurs et éléments UserInput | Conversion du callback | Après copie des données ; Dispose si requis, puis fermeture des handles |
| Événement utilisateur ou queue de l'appelant | Appelant | Après fermeture du service et arrêt de ses utilisateurs |

Une copie du builder partage son handle ; elle n'en devient pas propriétaire indépendamment.
Fermer un alias invalide les autres. Un propriétaire unique organise la fermeture et évite les appels concurrents avec Close.
Fermer un handle LabVIEW .NET, appeler Dispose et désabonner un événement sont des opérations distinctes.
Les garanties actuelles de fermeture ne constituent pas une preuve d'absence de fuite mémoire.

## Callbacks : conception restante

Le service devra conserver un gestionnaire concret injecté dans Initialize, enregistrer les abonnements et convertir les arguments natifs en `Activation.ctl` avant d'appeler Handle Activation.
Les arguments d'activation restent une chaîne brute : aucun format de parsing n'est imposé à tous les gestionnaires.
Le gestionnaire doit retourner rapidement et déléguer le travail long à une boucle de l'appelant.
Il ne doit pas attendre le thread qui ferme le service ni appeler sa fermeture depuis le callback.
Les modifications d'une copie du gestionnaire ne constituent pas un état partagé ; les adaptateurs utiliseront des mécanismes de communication explicites.
Le service ne détruit jamais implicitement les queues ou événements de l'appelant.

Le futur protocole de fermeture devra :

1. Passer le contexte partagé en Closing pour refuser de nouveaux envois.
2. Désabonner les événements sans détruire le contexte des callbacks engagés.
3. Attendre leur fin de façon bornée, sans conserver un verrou nécessaire à ces callbacks.
4. En cas de timeout, conserver les ressources encore utilisées et permettre une nouvelle tentative.
5. Libérer les références persistantes puis passer en Closed.

Initialize devra appliquer un rollback similaire en cas d'acquisition partielle.
Cette synchronisation n'est pas encore implémentée. L'exemple ferme actuellement le service immédiatement après Show : il devra attendre la fin de l'interaction lorsque les callbacks seront raccordés.

## Passages de relais

Enregistrer les VIs avant de changer de main. Ne pas modifier le même VI simultanément dans l'IDE et par les outils.
Les fichiers enregistrés font foi. Les intermédiaires de génération restent dans `_review`, hors versionnement ; ils ne doivent pas servir à régénérer les VIs modifiés à la main.
