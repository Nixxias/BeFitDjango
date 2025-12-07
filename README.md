Befit - Aplikacja Treningowa
Befit to aplikacja internetowa stworzona w oparciu o framework Django, służąca do zarządzania treningami, śledzenia postępów oraz monitorowania statystyk aktywności fizycznej.

🛠️ Użyte Technologie
Projekt został zrealizowany przy użyciu następującego stosu technologicznego:

Język programowania: Python 3.13 

Backend Framework: Django 4.2+ 

Baza danych: SQLite3 

Frontend: HTML5, CSS3 

Zarządzanie zależnościami: plik requirements.txt 

Dane początkowe (Fixtures): JSON (TrainingTypes.json) 

🚀 Funkcjonalności
Aplikacja oferuje następujące możliwości:

System użytkowników: Rejestracja i logowanie użytkowników.

Zarządzanie ćwiczeniami: Przeglądanie typów ćwiczeń (Cardio, Siłowe, Joga itp.).

Dziennik treningowy: Dodawanie i zapisywanie odbytych sesji treningowych oraz konkretnych ćwiczeń.

Statystyki: Podgląd statystyk treningowych.

⚙️ Instrukcja Instalacji i Konfiguracji
Aby uruchomić aplikację na swoim komputerze, postępuj zgodnie z poniższymi krokami:

1. Pobranie projektu
Sklonuj repozytorium na swój komputer: 

git clone https://github.com/Nixxias/BefitDjango.git 

cd BefitDjango

2. Utworzenie wirtualnego środowiska (Zalecane)
Dobrą praktyką jest utworzenie izolowanego środowiska dla bibliotek Pythona.

Windows:
python -m venv venv
venv\Scripts\activate

macOS / Linux:
python3 -m venv venv
source venv/bin/activate

3. Instalacja wymaganych bibliotek
Zainstaluj Django i inne potrzebne pakiety zapisane w pliku requirements.txt:
pip install -r requirements.txt

4. Konfiguracja Bazy Danych
To najważniejszy krok. Należy utworzyć tabele w bazie danych oraz załadować początkowe typy ćwiczeń.
Uruchom komendę: 

python manage.py migrate 

Uwaga: Dzięki skonfigurowanej migracji danych, powyższa komenda automatycznie załaduje listę 10 typów ćwiczeń (Cardio, Siłowe, Joga, itp.) z pliku TrainingTypes.json. 

(Opcjonalnie) Jeśli z jakiegoś powodu typy ćwiczeń się nie pojawią, możesz załadować je ręcznie komendą:
python manage.py loaddata workout/fixtures/TrainingTypes.json

5. Utworzenie konta Administratora (Superuser)
Aby mieć pełny dostęp do panelu administracyjnego Django: 

python manage.py createsuperuser 

Postępuj zgodnie z instrukcjami na ekranie (podaj nazwę użytkownika, e-mail i hasło). 

6. Uruchomienie serwera
Teraz możesz uruchomić aplikację: 
python manage.py runserver
