FROM node:18-alpine as build-stage
RUN apk update && apk add git
RUN git clone --branch '2024.6.0' https://github.com/OpenEMS/openems.git
WORKDIR /openems/ui
RUN npm install -g @angular/cli
RUN npm install
# ADD language.ts src/app/shared/type/language.ts
RUN ng build -c "openems,openems-edge-dev"
# RUN ng build -c "openems,openems-edge-prod,prod"

FROM nginx:latest
COPY --from=build-stage /openems/ui/target /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf