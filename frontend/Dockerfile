FROM node:18-alpine

WORKDIR /home/fsuv-bc-frontend

COPY . .

RUN npm install

RUN npm run build

RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]