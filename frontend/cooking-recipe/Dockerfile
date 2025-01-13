FROM node:18

WORKDIR /app

# Installiere Abhängigkeiten
COPY package*.json ./
RUN npm install

# Kopiere den gesamten Quellcode ins Arbeitsverzeichnis
COPY . .

# Exponiere den Entwicklungsport
EXPOSE 5173

# Standardkommando für die Entwicklung
CMD ["npm", "run", "dev"]
