
1.
2. KEINE VERBEN
Da die HTTP Methoden wie GET POST DELETE schon was getan wird angeben,
brauchen wir diese Information nicht im Endpunktnamen wiederholen.

## 3. Logisches Nesting von Endpoints
Endpunkte die eine auf gleicher Information aufbauen sollten gemäß der Information gruppiert werden.
Auch wenn dies nicht dem Datenbankschema entspricht ist es Good practice und verringert die potentielle Angrifffläche

Bsp:
News-Webseite mit Artikeln und Kommentaren
falsch /articles & /comments?articleId=...
richtig /articles/:articleId/comments

Dennoch sollte man es mit dem Nesting nicht übertreiben, nach max 3 Nesting könnte man auch die Resourcen-Quelle in der Antwort zurückliefern.
falsch /articles/:articleId/comments/:commentId/author 
stattdessen richtig /articles/:articleId/comments und /users/:userId in der Response zurückgeben
4.
5. FILTERN UND PAGINIERUNG
Zum schonen des Servers soll es möglich sein, nur bestimmt Daten zu holen.
Bei grossen Datenmengen sollen die Daten in Batches zurückgegeben werden, damit 
6. Maintain good security practices
7. Cache data to improve performance
8. VERSIONING
