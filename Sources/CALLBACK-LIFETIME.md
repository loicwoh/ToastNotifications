# OnActivated : conversion et durée de vie

Le callback natif conserve son connecteur à quatre entrées et appelle la méthode dynamique `ActivationHandler.Handle Activation` sur l'objet fourni lors de l'enregistrement. Les helpers propres aux activations restent dans `ToastService` ; les opérations génériques de réflexion et de nettoyage sont regroupées dans `Reflection DotNet.lvlib`.

## Propriété des références

| Référence | Propriétaire et traitement |
|---|---|
| `Event Data.e`, `Control Ref` | Empruntées au mécanisme de callback. Aucune fermeture ni aucun `Dispose` dans le callback. |
| `Type`, type d'interface, `PropertyInfo`, `MethodInfo` | Acquis par les helpers de réflexion, fermés par ces mêmes helpers après usage, même en cas d'erreur. |
| Valeur renvoyée par `GetValue` ou `Invoke` | Référence acquise, fermée par l'appelant après copie ou consommation. Les sorties `reference out` des nœuds ne sont pas des acquisitions supplémentaires. |
| Collection `UserInput` | Acquise par le convertisseur, empruntée par l'énumération, fermée par le convertisseur. |
| Énumérateur | Acquis par l'énumération ; `Dispose` si `IDisposable` est disponible, puis fermeture de la référence. |
| Résultat de `MoveNext`, élément `Current`, valeurs `Key` et `Value` | Fermés après chaque utilisation, y compris sur les chemins d'erreur. |

`Close Reference` libère le handle LabVIEW ; ce n'est pas un appel à `IDisposable.Dispose`. Le helper de fermeture ignore les références invalides et travaille aussi avec une erreur entrante. L'erreur principale garde la priorité lors de la fusion des erreurs de nettoyage.

Les sorties `object out` des lecteurs de propriétés sont des alias empruntés de `object in`, conservés même avec une erreur entrante. Elles n'impliquent aucune acquisition supplémentaire. La sortie `value` est la valeur acquise : c'est elle que l'appelant doit libérer. Les noms spécifiques `Activation Event Args`, `User Input Collection`, `User Input Enumerator`, `Object Type`, `Property Info` et `Method Info` distinguent les rôles malgré les références transportées comme `System.Object`.

## Données remises au handler

`Convert Activation Event` copie `Argument` dans `Activation.Arguments` et parcourt tous les éléments de `UserInput` dans `Activation.User Inputs`. Il ne lit `Current` qu'après un `MoveNext` réussi et vrai. Une collection nulle donne un tableau vide. Une propriété nulle à convertir en chaîne produit une erreur ; aucune politique de substitution silencieuse n'est ajoutée.

La conversion s'arrête à la première erreur et conserve les entrées déjà copiées. Les références temporaires sont nettoyées avant l'appel du handler. Le payload contient uniquement `Arguments` et `User Inputs` ; l'erreur de conversion est transmise séparément à l'entrée d'erreur du handler. `Last Callback Error` expose sa sortie d'erreur pour diagnostic ; ce n'est pas une file d'événements.

Pour personnaliser la réaction, surcharger `Handle Activation` dans une classe enfant et passer cette instance à l'enregistrement des événements. Le handler travaille sur les données LabVIEW et n'a pas à conserver de référence .NET issue du callback. La boîte de dialogue de démonstration actuellement présente dans le handler de base bloque le retour du callback jusqu'à sa fermeture.

## Vérifications et limites

Les 15 helpers, le callback, l'enregistrement et l'exemple sont exécutables dans LabVIEW 2026, vérifiés via le backend pylabview/VI Server. Les aides contextuelles et les bannières d'icônes ont été complétées. Les classes et bibliothèques possèdent chacune un dossier physique plat.

Une sonde ponctuelle de réflexion .NET a lu `Lifecycle probe`, parcouru son premier caractère `L`, obtenu `MoveNext = True`, puis effectué le nettoyage sans erreur. L'utilisateur a ensuite confirmé le fonctionnement du toast avec un champ texte et un bouton. Aucun framework de tests unitaires n'est ajouté.

Après arrêt de l'exemple, le callback est resté en état `eRunning` et verrouillait l'édition. Une exécution unique de `System.GC.Collect()` sans argument dans un VI séparé l'a fait passer à `eIdle`, sans quitter LabVIEW et sans erreur. L'exemple effectue désormais cette collecte après les fermetures ; le service ne l'appelle pas dans le callback.

La capture de plusieurs champs et la stabilité mémoire sur une série d'activations restent à vérifier. Le désenregistrement pendant un callback en cours et la protection contre plusieurs enregistrements demandent encore une passe dédiée. La gestion des temporaires de composition, dont le handle du bouton créé par `Add Bouton`, reste également à durcir. Le succès d'une collecte ne prouve pas l'absence de fuite mémoire.
