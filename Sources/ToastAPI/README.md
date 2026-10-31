# ToastAPI

Bibliothèque LabVIEW 2026 pour construire et afficher des notifications Windows en encapsulant les appels .NET du toolkit Microsoft.
Ouvrir `ToastAPI.lvproj`. Le projet historique `../ToastNotifications.lvproj` et son dossier `SandBox` sont conservés.

## API actuelle

- `ToastBuilder` possède la référence native `ToastContentBuilder`. Ses méthodes appellent directement le toolkit ; aucune description intermédiaire LabVIEW n'est stockée.
- `ToastService.Show` reçoit un builder et délègue l'affichage à `ToastBuilder.Show`.
- `ActivationHandler.Handle Activation` définit le point d'extension pour les futures activations. La méthode de base renvoie l'erreur 7621.
- `ToastService.Initialize` crée actuellement un service par défaut : le paramètre `Handler` n'est pas encore conservé et aucun callback n'est enregistré.
- `ToastService.Close` est actuellement une opération sans effet qui conserve l'erreur entrante.

## Exemple avec les classes

Ouvrir `Examples/Build Toast With Classes.vi`. Le diagramme enchaîne :

1. `ToastBuilder.Create`.
2. Deux appels à `ToastBuilder.Add Text`.
3. `ToastBuilder.Get XML`.
4. `ToastService.Initialize`, puis `ToastService.Show`.
5. `ToastService.Close`, puis `ToastBuilder.Close`.

Exécuter cet exemple peut afficher une notification Windows. Il ne reçoit pas encore les réponses de l'utilisateur.
Le fil d'erreur ordonne les appels et les fermetures. `Toast XML` expose le contenu sérialisé.
`Examples/Native Toast Example.vi` illustre les appels natifs avec arguments, champ texte et bouton, sans callback.

## Références et fermeture

`Create` libère un ancien handle avant réinitialisation. `Add Text` modifie immédiatement le builder natif.
`Get XML` libère sa référence temporaire vers le contenu. `Show` emprunte le builder sans le fermer.
Ces opérations sont ignorées en présence d'une erreur entrante.
`Close` travaille aussi avec une erreur entrante, qu'il conserve, et accepte un objet vide ou déjà fermé.
Les erreurs de nettoyage sont fusionnées avec l'erreur entrante ; aucun code n'est masqué.

Les accesseurs du handle sont privés et utilisés via des nœuds de propriétés de classe.
Une copie de la classe partage le même handle .NET : elle ne crée pas un builder indépendant.
Un seul propriétaire doit gérer sa durée de vie. Fermer un alias invalide les autres alias.
Pour obtenir un builder indépendant, appeler `Create` sur un nouvel objet.
Aucun appel concurrent avec `Close` n'est autorisé par le contrat actuel.

Le dossier virtuel `Native VIs` de la bibliothèque contient les appels techniques du toolkit.
`Activation.ctl` et `Argument.ctl` restent disponibles pour le contrat de callback.
L'ancienne classe LabVIEW `ToastContent`, son exemple et ses typedefs de construction ont été retirés.
Le type .NET `ToastContent` utilisé en interne par le toolkit est distinct et reste nécessaire à `Get XML`.

## État et vérification

Le parcours construction/XML a été exécuté sans erreur, y compris avec fermeture répétée et conservation d'une erreur entrante.
Les VIs d'affichage et l'exemple complet ont été vérifiés comme exécutables sans déclencher de notification pendant la revue.
Les descriptions précisent l'état actuel des callbacks et la propriété des références.
Aucun test unitaire ni dépendance Caraya n'est livré. Ces contrôles ne constituent pas une mesure des fuites mémoire ou de concurrence.

Voir [ARCHITECTURE.md](ARCHITECTURE.md) pour les responsabilités et le futur cycle des callbacks.
