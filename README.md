# Mentor AI RAG

Aplicație Python care ajută persoanele interesate de o carieră în IT printr-o colecție de ghiduri, căutare semantică și un mentor AI. Proiect realizat la finalul cursului de Python și Agentic AI.

Interfața și răspunsurile AI sunt în limba română. Aplicația combină o interfață Streamlit, un backend FastAPI, stocarea în MySQL și căutarea semantică prin ChromaDB și embeddings OpenAI.

## Funcționalități

- Vizualizarea ghidurilor de carieră și filtrarea după categorie.
- Adăugarea ghidurilor, cu validarea datelor și verificarea titlurilor duplicate.
- Ștergerea ghidurilor din MySQL și din indexul de căutare.
- Căutarea după sens și afișarea ghidurilor găsite împreună cu distanțele lor.
- Conversația cu mentorul AI și consultarea textelor recuperate ca surse.
- Continuarea conversației folosind istoricul păstrat în sesiunea Streamlit.

Cele opt ghiduri inițiale acoperă CV-ul, portofoliul GitHub, LinkedIn, interviurile comportamentale și tehnice, negocierea salarială, rolurile din IT și primele 90 de zile la un loc de muncă nou.

## Cum funcționează

MySQL păstrează ghidurile complete. La pornirea backend-ului, aplicația creează tabela dacă aceasta nu există, încarcă fișierele inițiale dacă tabela este goală și indexează toate ghidurile salvate într-o colecție Chroma păstrată în memorie.

În pagina **Cautare**, backend-ul găsește ghiduri similare folosind modelul de embeddings `text-embedding-3-small` și returnează titlurile, textele și distanțele. O distanță mai mică indică o potrivire mai apropiată; nu reprezintă un procent de încredere.

În pagina **Mentor AI**, un agent LangChain care folosește modelul `gpt-4.1-mini` poate apela instrumentul `cauta_in_ghiduri`. Instrucțiunile de sistem îi cer să formuleze răspunsurile despre carieră pe baza ghidurilor recuperate și să citeze titlurile acestora. Rezultatele instrumentului pot fi consultate în secțiunea **Surse**. Aceste instrucțiuni reduc răspunsurile fără suport în ghiduri, dar nu garantează corectitudinea tuturor informațiilor.

RAG înseamnă *Retrieval-Augmented Generation*: recuperarea documentelor relevante și folosirea lor drept context pentru generarea unui răspuns.

## Tehnologii

| Componentă | Tehnologie |
| --- | --- |
| Interfață | Streamlit |
| API HTTP | FastAPI și Uvicorn |
| Validarea datelor | Pydantic |
| Bază de date | MySQL, SQLAlchemy și PyMySQL |
| Index semantic | ChromaDB |
| Embeddings | OpenAI `text-embedding-3-small` |
| Agent AI | LangChain și OpenAI `gpt-4.1-mini` |
| Cereri între interfață și API | Requests |

## Fișierele proiectului

| Cale | Rol |
| --- | --- |
| `s50_app.py` | Endpoint-urile API și pornirea backend-ului |
| `s50_model.py` | Modelul bazei de date, sesiunile, datele inițiale și operațiile cu ghiduri |
| `s50_schema.py` | Schemele de validare pentru cereri și răspunsuri |
| `s50_rag.py` | Embeddings, indexare, căutare și ștergere din index |
| `s50_agent.py` | Agentul AI, instrumentul de căutare și instrucțiunile de sistem |
| `s50_ui.py` | Navigarea între paginile Streamlit |
| `comun.py` | Clientul HTTP comun și tratarea erorilor API |
| `s50_pages/` | Paginile pentru listare, adăugare, căutare și conversație |
| `ghiduri_initiale/` | Cele opt fișiere text cu ghidurile inițiale |

## Instalare și configurare locală

Sunt necesare Python cu versiuni compatibile ale bibliotecilor de mai jos, un server MySQL pornit și o cheie API OpenAI cu acces la modelele de conversație și embeddings configurate. Utilizarea API-ului OpenAI necesită facturare sau credite API separate.

Comenzile următoare sunt pentru **Windows PowerShell**. Rulează-le din folderul principal al repository-ului, unde se află `s50_app.py`, `s50_ui.py` și folderul `ghiduri_initiale/`.

### 1. Descărcarea proiectului și instalarea dependențelor

```powershell
git clone https://github.com/ittechconstantin/Mentor-AI-RAG.git
cd Mentor-AI-RAG
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install fastapi uvicorn sqlalchemy pymysql cryptography pydantic streamlit requests chromadb langchain langchain-core langchain-openai
```

Dacă Python este disponibil prin comanda `python`, în loc de `py`, folosește `python -m venv .venv` pentru crearea mediului virtual. Versiunile dependențelor nu sunt fixate în prezent în repository.

### 2. Crearea bazei de date MySQL

Execută instrucțiunea următoare în MySQL Workbench sau într-un client MySQL, folosind un cont cu drepturi de creare a bazelor de date:

```sql
CREATE DATABASE IF NOT EXISTS curs
CHARACTER SET utf8mb4;
```

Aplicația creează automat tabela `s50_ghid`. Conexiunea implicită folosește utilizatorul `root`, serverul `localhost:3306` și baza de date `curs`.

### 3. Configurarea backend-ului

În terminalul PowerShell în care vei porni backend-ul:

```powershell
$env:OPENAI_API_KEY="CHEIA_TA_OPENAI"
$env:MYSQL_PASSWORD="PAROLA_TA_MYSQL"
```

Înlocuiește valorile exemplificative doar pe calculatorul tău. Nu introduce date reale de autentificare în fișierele sursă sau în commit-uri.

Pentru un alt cont MySQL sau o altă conexiune, setează variabila `DATABASE_URL`:

```powershell
$env:DATABASE_URL="mysql+pymysql://UTILIZATOR:PAROLA@localhost:3306/curs"
```

`DATABASE_URL` are prioritate față de `MYSQL_PASSWORD`. Dacă datele de autentificare incluse în URL conțin caractere speciale, acestea trebuie codificate pentru URL.

Codul actual citește direct variabilele de mediu. **Nu încarcă automat un fișier `.env`.** Variabilele PowerShell de mai sus se aplică terminalului curent și proceselor pornite din acesta.

### 4. Pornirea backend-ului

```powershell
.\.venv\Scripts\python.exe s50_app.py
```

La pornire, aplicația indexează ghidurile salvate și trimite cereri către API-ul de embeddings. Păstrează acest terminal deschis.

- API: [http://127.0.0.1:8005](http://127.0.0.1:8005)
- Documentație API interactivă: [http://127.0.0.1:8005/docs](http://127.0.0.1:8005/docs)

### 5. Pornirea interfeței

Deschide un al doilea terminal PowerShell în același folder al repository-ului:

```powershell
.\.venv\Scripts\python.exe -m streamlit run s50_ui.py
```

Accesează adresa locală afișată de Streamlit, de regulă [http://localhost:8501](http://localhost:8501). Backend-ul și interfața trebuie să rămână pornite simultan.

## Endpoint-uri API

| Metodă | Endpoint | Rol |
| --- | --- | --- |
| `GET` | `/ghiduri` | Listează ghidurile; acceptă filtrul opțional `categorie` |
| `POST` | `/ghiduri` | Creează un ghid și îl adaugă în index |
| `DELETE` | `/ghiduri/{ghid_id}` | Șterge ghidul și textul său din index |
| `GET` | `/cauta` | Caută semantic folosind `intrebare` și parametrul opțional `n`, între 1 și 5 |
| `POST` | `/chat` | Trimite agentului `mesaj` și, opțional, `istoric` |

Exemplu de corp al cererii pentru adăugarea unui ghid:

```json
{
  "titlu": "Pregatirea demonstratiei proiectului",
  "categorie": "Interviu",
  "continut": "Pregateste o demonstratie scurta a proiectului si explica rolul fiecarei componente, pornind de la interfata si continuand cu API-ul si baza de date."
}
```

Titlul trebuie să conțină între 3 și 200 de caractere, iar conținutul cel puțin 50 de caractere. Categoriile acceptate sunt `CV si portofoliu`, `Interviu`, `Negociere`, `Roluri IT`, `La job` și `Altele`.

## Scenariu de demonstrație

1. Deschide **Ghiduri** și selectează categoria **Interviu**.
2. În **Cautare**, introdu `Cum cer mai multi bani la angajare?` și consultă ghidurile găsite.
3. În **Mentor AI**, întreabă `Cum negociez salariul la prima oferta pentru un job junior in IT?` și deschide secțiunea **Surse**.
4. Adresează o întrebare de continuare în aceeași conversație.
5. Adaugă un ghid cu titlu unic, verifică apariția sa în listă și apoi șterge-l.

## Limitele versiunii actuale

- Aplicația este un proiect educațional destinat rulării locale. Nu include autentificare sau control al accesului pentru utilizatori.
- Datele MySQL persistă. Indexul Chroma este reconstruit la fiecare repornire a backend-ului, ceea ce presupune noi cereri de embeddings.
- Istoricul conversației este păstrat în sesiunea Streamlit și nu este salvat în MySQL.
- Căutarea returnează cele mai apropiate rezultate disponibile, fără un prag de relevanță. Ghidurile recuperate pot să nu răspundă unei întrebări fără legătură cu subiectele lor.
- Salvarea în baza de date și actualizarea indexului sunt operații separate. O eroare de indexare le poate lăsa temporar nesincronizate. Repornirea backend-ului reconstruiește indexul din MySQL.
- Verificările manuale locale au acoperit pornirea, listarea ghidurilor, căutarea semantică, un răspuns AI și adăugarea și ștergerea unui ghid. Repository-ul nu include o suită de teste automate.
