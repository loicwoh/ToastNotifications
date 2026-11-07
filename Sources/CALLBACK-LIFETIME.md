# OnActivated : notes de conversion et observations historiques

> Notes destinées à la maintenance, pas un second contrat utilisateur.
> Voir [le contrat courant](docs/site/callbacks.md), [ToastService](docs/site/api/toastservice.md)
> et [la carte des sources](docs/CONTENT-MAP.md). Les sondes et décomptes ci-dessous
> décrivent le développement initial ; la génération documentaire ne les réexécute pas.

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

La conversion s'arrête à la première erreur et conserve les entrées déjà copiées. Les références temporaires sont nettoyées avant l'appel du handler. Le payload contient uniquement `Arguments` et `User Inputs` ; l'erreur de conversion est transmise séparément à l'entrée d'erreur du handler. Le handler User Event relaie cette erreur à côté d'Activation. Il n'expose pas encore l'erreur de Generate User Event (#22) ; la classe actuelle n'a pas d'accesseur `Last Callback Error`.

Pour personnaliser la réaction, surcharger `Handle Activation` dans une classe enfant et passer cette instance à ToastService.Initialize ; Register For Events réutilise ensuite le handler initialisé stocké par le service. Le handler travaille sur les données LabVIEW et n'a pas à conserver de référence .NET issue du callback. Le handler de base actuel est sans action applicative ; l'ancien dialogue de démonstration a été retiré. Le handler applicatif doit retourner rapidement et transmettre les données vers sa boucle si nécessaire.

Un bouton ajouté avec `Add Link Button` utilise l'activation Protocol : Windows ouvre son URI sans remettre cette action au callback LabVIEW. Le clic sur le corps du toast est une activation applicative distincte ; le handler de base actuel n'affiche rien pour cette activation. L'exemple de lien conserve l'enregistrement du service et attend stop avant sa fermeture.

## Vérifications historiques et limites

Les 15 helpers, le callback, l'enregistrement et l'exemple sont exécutables dans LabVIEW 2026, vérifiés via le backend pylabview/VI Server. Les aides contextuelles et les bannières d'icônes ont été complétées. Les classes et bibliothèques possèdent chacune un dossier physique plat.

Une sonde ponctuelle de réflexion .NET a lu `Lifecycle probe`, parcouru son premier caractère `L`, obtenu `MoveNext = True`, puis effectué le nettoyage sans erreur. L'utilisateur a ensuite confirmé le fonctionnement du toast avec un champ texte et un bouton. Aucun framework de tests unitaires n'est ajouté.

Après arrêt de l'exemple, le callback est resté en état `eRunning` et verrouillait l'édition. Une exécution unique de `System.GC.Collect()` sans argument dans un VI séparé l'a fait passer à `eIdle`, sans quitter LabVIEW et sans erreur. L'exemple effectue désormais cette collecte après les fermetures ; le service ne l'appelle pas dans le callback.

La capture de plusieurs champs et la stabilité mémoire sur une série d'activations restent à vérifier. Le désenregistrement pendant un callback en cours et la protection contre plusieurs enregistrements demandent encore une passe dédiée. La gestion des temporaires de composition, dont le handle du bouton créé par `Add Bouton`, reste également à durcir. Le succès d'une collecte ne prouve pas l'absence de fuite mémoire.
