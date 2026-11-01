# Reprise dans LabVIEW

Ouvrir `ToastAPI.lvproj`, puis `Examples/Build Toast With Classes.vi`.
La première phase fournit le wrapper direct, un champ Reply, un bouton Répondre, l'enregistrement OnActivated, la conversion des données et le handler à dispatch dynamique injecté.

Saisir un texte et cliquer sur Répondre ; le handler de base est désormais sans action. Utiliser un handler dérivé pour consommer les données. Appuyer sur Stop. Le service est désenregistré et fermé, puis le builder fermé. Une collecte .NET termine l'exemple pour libérer la réservation du callback constatée sur ce poste.

Pour l'exemple de lien (#11), ouvrir `Examples/Toast With Link Button.vi` : le bouton **Open project on GitHub** utilise `ToastBuilder.Add Link Button` et ouvre l'URL via l'activation Protocol. Le natif utilise directement la surcharge AddButton(content, activationType, arguments), sans System.Uri ni handle de bouton séparé. Appuyer sur stop dans LabVIEW après le clic ; voir `Examples/Protocol Activation.md`. L'utilisateur a confirmé l'ouverture du lien.

Les dossiers physiques sont plats : ToastNotification, ToastBuilder, ToastService, ActivationHandler, Toast Native, Reflection DotNet et Examples. Chaque classe ou bibliothèque est placée avec ses membres. Les scopes restent des dossiers virtuels.
Les aides contextuelles décrivent les paramètres et la propriété des handles. Les documents README, ARCHITECTURE et CALLBACK-LIFETIME décrivent le comportement actuel.

Les interactions Windows ont été validées manuellement par l'utilisateur. Les 49 VIs sont exécutables après déplacement et sauvegarde des liens. Aucun framework de tests unitaires n'est ajouté.

Suite du travail : durcir la fermeture et les doubles enregistrements, organiser l'attente des callbacks en cours, fermer systématiquement les temporaires de composition et mesurer la mémoire sur des activations répétées (#16). Un handler applicatif devrait transférer les données vers sa propre boucle et retourner rapidement.

Enregistrer avant de rendre la main. Le prototype historique et SandBox restent conservés sous `Archive`, avec leurs dépendances. `_review` est ignoré par Git et ne constitue pas une dépendance du projet.
