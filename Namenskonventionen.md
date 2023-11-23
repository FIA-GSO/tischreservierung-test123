QUELLE: https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/

1. JSON für Request-Payload oder Response akzeptieren

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

4. Ordnungsgemäße Behandlung von Fehlern und Rückgabe beschreibender HTTP-Antwortcodes, um API-Benutzern klare Informationen zu liefern
   und die API-Stabilität aufrechtzuerhalten.
   Vermeiden Fehler unbehandelt zu lassen, um sicherzustellen,
   dass der Benutzer Probleme effektiv angehen und verwalten kann, ohne die Systemintegrität zu beeinträchtigen.

5. FILTERN UND PAGINIERUNG
   Zum schonen des Servers soll es möglich sein, nur bestimmt Daten zu holen.
   Bei grossen Datenmengen sollen die Daten in Batches zurückgegeben werden, damit

6. Maintain good security practices
   -SSL und TLS verwenden
   -Man sollte nicht mehr Daten zurückliefern als angefragt wird, also ein User soll nicht die Daten eines anderen Anfragen können/erhalten
   -Rollen/Grupper/User Permissions verwenden um Rechteverteilung bei der verschiedenen APIs zu verwalten

7. Cache data to improve performance
   Implementieren eines Caching-Mechanismus wie Flask-Caching oder In-Memory-Caching, um die Geschwindigkeit des Datenabrufs zu erhöhen.
   Aufnahme von Cache-Control-Informationen in die Kopfzeilen, um den Benutzer die effektive Nutzung des Caching-Systems zu ermöglichen und
   ein Gleichgewicht zwischen Performanz und potentiell veraltete Daten in produktiven Umgebungen zu schaffen.

8. VERSIONING
   Damit laufende Dienste Zeit haben, sich auf Änderungen in der API einzustellen soll
   es verschiedene Versionen der Endpunkte geben. Diese werden z.B. durch /v1/endpunktname und
   /v2/endpunktname differenziert. So ist die alte Version weiterhin verfügbar bis auf v2 umgestellt wird von Nutzern der API.
