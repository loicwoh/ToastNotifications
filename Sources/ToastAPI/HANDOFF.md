# Reprise dans LabVIEW

Branche : `feature/toastapi-contracts-content`.

Ouvrir `ToastAPI.lvproj`, puis `Examples/Build Toast With Classes.vi`.
Le diagramme construit un ToastBuilder, ajoute deux textes, lit le XML, initialise le service, affiche, ferme le service et ferme le builder.
L'exécution peut afficher une notification Windows. Aucune activation utilisateur n'est encore reçue.
L'ancien ToastContent LabVIEW et son exemple ont été retirés.

`Examples/Native Toast Example.vi` conserve un exemple de composition avec arguments, saisie et bouton via les VIs natifs.
La bibliothèque `ToastNotification.lvlib` regroupe les classes, les appels natifs, la DLL et les types de callback Activation/Argument.
Les accesseurs de la référence du builder sont privés. Les descriptions des VIs indiquent les responsabilités de fermeture et les limites actuelles.

La construction et la lecture du XML ont été vérifiées par exécution avant l'ajout de Show au parcours ; la fermeture répétée et l'erreur entrante ont été contrôlées.
Le parcours d'affichage est vérifié par compilation ; aucune notification n'est exécutée automatiquement lors de la revue.
Aucun test unitaire ni dépendance Caraya n'est livré. Il reste à vérifier les fuites mémoire et la concurrence.

Prochaine étape : conserver le handler dans Initialize, enregistrer et convertir le callback, puis définir l'attente et la fermeture du service.
Voir ARCHITECTURE.md pour la propriété des ressources et le protocole envisagé.
Enregistrer les VIs avant de rendre la main. Continuer sur la même branche jusqu'à la revue et la fusion.
