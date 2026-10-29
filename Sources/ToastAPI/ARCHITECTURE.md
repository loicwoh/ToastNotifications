# Architecture et contrats

Décisions des issues [#1](https://github.com/loicwoh/ToastNotifications/issues/1) et [#2](https://github.com/loicwoh/ToastNotifications/issues/2).

## Frontières

`ToastContent.lvclass` est une description LabVIEW par valeur. Son champ privé `Data` est lié à `Content Data.ctl`.
Les méthodes de construction et de validation sont statiques ; aucun héritage n'est requis pour composer un toast.
`Read Data` expose uniquement une copie de la description. Aucun accesseur d'écriture globale n'est exposé.
Les typedefs de paramètres `Argument`, `Text Input` et `Button` sont liés aux connecteurs des méthodes correspondantes.
Les éléments des tableaux de `Content Data` sont également liés à ces typedefs ; les entrées utilisateur d'`Activation` réutilisent la paire `Argument`.

`ToastService.lvclass` possède la future intégration Windows. Cette livraison ne lui attribue volontairement aucune fausse ressource ni indicateur d'initialisation.
La réflexion .NET, les métadonnées WinRT et la gestion des abonnements seront privées. Aucune référence .NET ne sera un terminal public.

`ActivationHandler.lvclass` définit le point d'extension `Handle Activation`, à dispatch dynamique.
Le service recevra un gestionnaire concret par injection dans `Initialize`.
La conversion du callback en `Activation.ctl` sera achevée avant d'appeler le gestionnaire.
Le gestionnaire ne devra ni rappeler `Close` dans le callback, ni bloquer en attendant le thread qui ferme le service.
Il devra déléguer un travail long à une boucle appelante.

## Connecteurs

Pattern 4815 : classe en haut à gauche (11), classe sortie en haut à droite (3), erreur entrée en bas à gauche (8), erreur sortie en bas à droite (0).
Paramètre principal additionnel à gauche (10). Snapshot de données à droite (2).

| Propriétaire | Méthode | Entrées supplémentaires | Sorties supplémentaires | Contrat |
| --- | --- | --- | --- | --- |
| ToastContent | Create | — | — | Réinitialise le contenu si aucune erreur entrante |
| ToastContent | Add Text | Text : chaîne | — | Ajoute un élément texte |
| ToastContent | Add Argument | Argument.ctl | — | Ajoute une paire clé/valeur |
| ToastContent | Add Text Input | Text Input.ctl | — | Ajoute un champ texte |
| ToastContent | Add Button | Button.ctl | — | Ajoute un bouton |
| ToastContent | Validate | — | — | Lecture seule ; première erreur structurelle |
| ToastContent | Read Data | — | Content Data.ctl | Copie de la description ; valeur par défaut si erreur entrante |
| ToastService | Initialize | Handler : ActivationHandler | — | Futur : acquérir les ressources et conserver le gestionnaire ; actuellement erreur 7620 |
| ToastService | Show | Content : ToastContent | — | Futur : valider puis afficher ; actuellement erreur 7620 |
| ToastService | Close | — | — | Actuellement aucune ressource : opération sans effet, erreur entrante conservée |
| ActivationHandler | Handle Activation | Activation.ctl | — | Surcharge dynamique ; méthode de base : erreur 7621 |

Les terminaux de classe du gestionnaire sont dynamiques, ceux du service sont statiques.
Les états intermédiaires du builder sont autorisés ; `Show` devra appeler `Validate` même si l'appelant l'a déjà fait.
Les arguments d'activation restent une chaîne brute : ne pas imposer un format de parsing à tous les gestionnaires.

## Propriété des ressources — contrat du futur backend

| Ressource | Propriétaire | Fin de vie |
| --- | --- | --- |
| Description du contenu, arguments et activation convertie | Valeurs LabVIEW | Automatique ; aucun Close |
| Abonnement .NET au callback et contexte du callback | ToastService | Désabonnement, puis attente des callbacks engagés, puis fermeture des références |
| Références persistantes de l'intégration Windows | ToastService | Close, ou rollback d'Initialize |
| Références Type / PropertyInfo / MethodInfo / objets temporaires | Méthode qui les acquiert | Nettoyage en sortie normale et en sortie sur erreur |
| Énumérateur et éléments de UserInput acquis par le wrapper | Conversion du callback | Après copie des données ; Dispose si requis, puis fermeture des références acquises |
| sender et arguments fournis au callback | Empruntés à l'infrastructure | Ne pas Dispose arbitrairement ; documenter séparément les handles acquis et leur fermeture |
| Objet ActivationHandler conservé | Valeur privée du service | Relâché après la fin des callbacks ; aucun transfert implicite des ressources qu'il référence |
| Événement utilisateur / queue de l'appelant | Appelant | Après fermeture du service et arrêt des utilisateurs ; le service ne les détruit jamais |

Une copie du service ne deviendra pas un propriétaire indépendant des mêmes handles. Le programme conservera un unique fil propriétaire pour Initialize/Show/Close.
La synchronisation interne du contexte de callback sera définie lors de l'implémentation : une simple copie de booléen dans une classe par valeur ne suffit pas à partager l'état de fermeture.
Les modifications du gestionnaire faites dans une copie du callback ne seront pas considérées comme un état automatiquement partagé avec l'appelant.
Les adaptateurs fournis ultérieurement utiliseront des mécanismes de communication explicites.

## Fermeture prévue

1. Passer l'état partagé en `Closing` pour refuser les nouveaux envois.
2. Désabonner l'événement .NET sans détruire prématurément le contexte du callback.
3. Attendre de façon bornée les callbacks déjà engagés. Ne pas attendre sous un verrou nécessaire à ces callbacks.
4. En cas de timeout, conserver les ressources encore utilisées et permettre une nouvelle tentative de Close : ne pas libérer des objets encore en service.
5. Libérer les ressources persistantes et effacer leurs handles ; passer en `Closed`.

Close devra rester idempotent et effectuer le nettoyage malgré une erreur entrante.
L'erreur primaire sera préservée ; les erreurs de nettoyage devront rester consultables dans un diagnostic de fermeture à définir avec le backend.
Initialize devra appliquer le même nettoyage en cas d'acquisition partielle. Un échec ne devra pas être masqué par une seconde erreur de nettoyage.
Fermer un handle LabVIEW .NET, appeler Dispose et désabonner un événement sont des actions distinctes : la liste exacte sera vérifiée objet par objet.

**Ce protocole est un contrat de conception, pas une garantie déjà testée sur WinRT.**
La présente version pure LabVIEW n'alloue aucune référence .NET ; elle ne permet donc pas encore de démontrer l'absence de fuite du futur backend.

## Passages de relais

Enregistrer les VIs avant de changer de main. Ne pas modifier le même VI simultanément dans l'IDE et par les outils.
Les `.vi` enregistrés sont les fichiers de travail et font foi. Les intermédiaires de génération restent dans `_review/authoring`, hors versionnement.
Ne pas régénérer des VIs modifiés à la main à partir de ces intermédiaires devenus obsolètes.
