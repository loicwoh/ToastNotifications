# Reprise dans LabVIEW

Validation de l'exemple Reply (#7) : l'utilisateur confirme le comportement attendu lors d'un clic à côté du toast, de sa fermeture et d'une interaction depuis l'historique des notifications Windows. Il confirme également une soumission vide avec la clé `Reason` présente et une valeur vide, ainsi que la restitution exacte de `Réponse & pièce <manquante> "à fournir"`. Une fermeture n'est pas présentée comme générant un callback d'activation. Le bouton Send standard sous le champ est le périmètre livré ; le rendu inline n'est pas implémenté.

Exemple de saisie #7 : `Examples/Toast With Reply.vi` ajoute un champ `Reason` et un bouton **Send** avec `action=reject&requestId=42`. Il réutilise UserEventActivationHandler et la boucle de réception. Les captures utilisateur montrent la paire `Reason` / `too bussy` reçue. Le guide `docs/example-guides/Reply Input.md` et l'aide du VI reflètent le code et les validations rapportées. L'ancien `Build Toast With Classes.vi` est conservé. Les garanties de fermeture concurrente et de diagnostic d'envoi restent suivies dans #16/#22.

Ouvrir `Toast Notifications.lvproj`, puis `Development Examples/Build Toast With Classes.vi`.
La première phase fournit le wrapper direct, un champ Reply, un bouton Répondre, l'enregistrement OnActivated, la conversion des données et le handler à dispatch dynamique injecté.

Saisir un texte et cliquer sur Répondre ; le handler de base est désormais sans action. Utiliser un handler dérivé pour consommer les données. Appuyer sur Stop. Le service est désenregistré et fermé, puis le builder fermé. Une collecte .NET termine l'exemple pour libérer la réservation du callback constatée sur ce poste.

Pour l'exemple de lien (#11), ouvrir `Examples/Toast With Link Button.vi` : le bouton **Open project on GitHub** utilise `ToastBuilder.Add Link Button` et ouvre l'URL via l'activation Protocol. Le natif utilise directement la surcharge AddButton(content, activationType, arguments), sans System.Uri ni handle de bouton séparé. Appuyer sur stop dans LabVIEW après le clic ; voir `docs/example-guides/Protocol Activation.md`. L'utilisateur a confirmé l'ouverture du lien.

Les dossiers physiques sont plats : ToastNotification, ToastBuilder, ToastService, ActivationHandler, Toast Native, Reflection DotNet et Examples. Chaque classe ou bibliothèque est placée avec ses membres. Les scopes restent des dossiers virtuels.

L'exemple #6, `Examples/Toast With Multiple Actions.vi`, contient Accept/Reject et `Set Activation Arguments` pour le corps. `ToastService.Initialize` reçoit et initialise le handler, puis l'exemple récupère le User Event de l'instance initialisée. La boucle affiche `Activation` et `error` jusqu'à stop. Le handler sous `PlugIns/UserEventActivationHandler` possède le User Event ; l'appelant possède son enregistrement. Sans champ de saisie, User Inputs vide est attendu. Les actions des boutons, le corps avec `action=open&requestId=42` et Stop/relance ont été confirmés manuellement. Voir `docs/example-guides/Multiple Actions.md`. Les erreurs d'envoi, les références invalides et la fermeture concurrente restent à vérifier dans #22/#16.
Les aides contextuelles décrivent les paramètres et la propriété des handles. Les documents README, ARCHITECTURE et CALLBACK-LIFETIME décrivent le comportement actuel.

Les interactions Windows ont été validées manuellement par l'utilisateur. Les 49 VIs sont exécutables après déplacement et sauvegarde des liens. Aucun framework de tests unitaires n'est ajouté.

Suite du travail : durcir la fermeture et les doubles enregistrements, organiser l'attente des callbacks en cours, fermer systématiquement les temporaires de composition et mesurer la mémoire sur des activations répétées (#16). Un handler applicatif devrait transférer les données vers sa propre boucle et retourner rapidement.

Enregistrer avant de rendre la main. Le prototype historique et SandBox restent conservés sous `Archive`, avec leurs dépendances. `_review` est ignoré par Git et ne constitue pas une dépendance du projet.
