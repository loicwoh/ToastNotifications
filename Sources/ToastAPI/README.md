# ToastAPI

Bibliothèque LabVIEW 2026 en cours de construction. Ouvrir `ToastAPI.lvproj`.
Le projet historique `../ToastNotifications.lvproj` et son dossier `SandBox` sont conservés.

## État livré

- `ToastContent` : description par valeur, ajout de texte, arguments, champs texte et boutons, validation.
- `ActivationHandler` : contrat à dispatch dynamique pour injecter le traitement des activations.
- `ToastService` : connecteurs du futur service et contrat de fermeture. **Aucun backend Windows n'est implémenté ici.**
- `Initialize` et `Show` retournent explicitement l'erreur 7620. Ils n'affichent pas de toast et n'enregistrent aucun callback.
- La méthode de base `Handle Activation` retourne l'erreur 7621. Créer un descendant et la surcharger.

## Construire un contenu

Un objet `ToastContent` par défaut est vide. `Create.vi` peut aussi réinitialiser un objet existant.
Chaîner le fil de classe et le fil d'erreur dans cet ordre, par exemple :

1. `Add Text` : texte de la notification.
2. `Add Argument` : cluster `{Key, Value}` pour les arguments associés au corps du toast.
3. `Add Text Input` : `{ID, Placeholder, Default Text}` ; par exemple `tbReply`.
4. `Add Button` : `{Label, Arguments, Text Input ID}` ; par exemple `{Reply, action=reply, tbReply}`.
5. `Validate` : contrôler le résultat avant son utilisation.
6. `Read Data` : obtenir une copie typée de la description, sans référence .NET.

Les opérations `Add` autorisent un état intermédiaire incomplet : un bouton peut être ajouté avant le champ qu'il référence.
Elles conservent l'ordre d'ajout et, en cas d'erreur entrante, rendent le contenu inchangé.
Les arguments du corps sont conservés comme paires de chaînes ; aucune sérialisation ni échappement XML n'est effectué à cette étape.
Les arguments d'un bouton sont une chaîne opaque appartenant à l'application, indépendante des arguments du corps.
Une association `Text Input ID` vide représente un bouton ordinaire.

`ToastContent` ne nécessite pas de `Close`. Une branche du fil donne une description indépendante par valeur.
Ne pas confondre ce comportement avec celui du futur service qui possédera des références partagées.

## Validation

La validation est déterministe et retourne la première erreur dans l'ordre suivant.
Une erreur entrante (`status = true`) est toujours conservée. Sans violation, un avertissement entrant est conservé aussi.

| Code | Règle |
| --- | --- |
| 7601 | Au moins un élément texte |
| 7602 | Aucun élément texte vide |
| 7603 | Aucune clé d'argument vide |
| 7604 | Pas de clé d'argument dupliquée |
| 7605 | Aucun identifiant de champ texte vide |
| 7606 | Pas d'identifiant de champ texte dupliqué |
| 7607 | Au plus cinq champs texte |
| 7608 | Au plus cinq boutons |
| 7609 | Aucun libellé de bouton vide |
| 7610 | Toute association non vide d'un bouton désigne un champ texte existant |

Les comparaisons d'identifiants et de clés respectent la casse. Une chaîne d'espaces n'est pas considérée vide.
Les règles de texte non vide et d'unicité des arguments sont des choix de cette API.
Les limites de cinq inputs et de cinq boutons proviennent du [schéma Microsoft](https://learn.microsoft.com/windows/apps/design/shell/tiles-and-notifications/toast-schema).
La validation ne garantit ni le rendu Windows, ni la validité de futurs attributs XML, ni la taille finale du payload, ni le déploiement.
Images, audio, sélection, activation par protocole et mise à jour de toast sont hors de cette version.

## Extension et ressources

Voir [ARCHITECTURE.md](ARCHITECTURE.md) pour les connecteurs, les responsabilités, les règles de propriété et le protocole de fermeture prévu.
L'exemple `Examples/Build Reply Content.vi` construit la description sans afficher de toast. Examiner `Content Data` et `error out`, modifier les entrées puis le relancer manuellement.
Aucun test unitaire ni dépendance Caraya n'est livré, conformément au choix du projet. La vérification automatique se limite au chargement des VIs et à leurs connecteurs.
