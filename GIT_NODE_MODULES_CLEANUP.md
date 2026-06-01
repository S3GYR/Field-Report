# GIT_NODE_MODULES_CLEANUP

Date : 2026-06-01

---

## Contexte

`frontend/node_modules/` était versionné dans Git. Il représentait plus de 99 % des fichiers du dépôt (13 210 fichiers sur 13 359).

---

## Actions réalisées

### 1. Mise à jour du `.gitignore`

Ajout des règles :

```
node_modules/
frontend/node_modules/
```

### 2. Retrait de l'index Git

```bash
git rm -r --cached frontend/node_modules
```

**Fichiers retirés** : 13 210

**Fichiers conservés localement** : oui (`frontend/node_modules/` reste sur disque)

---

## Résultat

| Métrique | Avant | Après | Delta |
|----------|-------|-------|-------|
| Fichiers versionnés | 13 359 | 151 | −13 208 |
| Pourcentage node_modules | 98.9 % | 0 % | −98.9 % |

---

## Vérification

```bash
git ls-tree -r HEAD --name-only | wc -l
```

**Résultat** : 151 fichiers versionnés.

---

## Fichiers conservés dans frontend/

- `Dockerfile`
- `package.json`
- `package-lock.json`
- `tsconfig.json`
- `tsconfig.node.json`
- `vite.config.ts`
- `public/`
- `src/`

Aucun code source frontend supprimé. `package.json` et `package-lock.json` conservés.

---

## Commit

| Attribut | Valeur |
|----------|--------|
| Hash | `b7dafa0` |
| Message | `Remove node_modules from repository` |
| Branche | `v1.0.1-dev` |

---

## Notes

- `npm install` régénère `frontend/node_modules/` localement à partir de `package-lock.json`.
- Le dépôt est désormais propre et cloneable rapidement.
- Les futurs `git add frontend/` n'importeront plus `node_modules/` grâce à `.gitignore`.
