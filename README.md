# dates-rest-API
## Heroku API
API avaliable here:
> [dates-rest-api.herokuapp.com/](https://dates-rest-api.herokuapp.com/)

## Endpoints
- **GET** [/api/v1/dates/](https://dates-rest-api.herokuapp.com/api/v1/dates/)
- **GET** [/api/v1/popular/](https://dates-rest-api.herokuapp.com/api/v1/popular/)
- **POST** [/api/v1/dates/](https://dates-rest-api.herokuapp.com/api/v1/dates/)  
With following body:
```json
{
"month": $month_number,
"day": $day_number,
}
```
- **DELETE** [/api/v1/dates/$id/](https://dates-rest-api.herokuapp.com/api/v1/dates/$id/)  
Where `$id` is id of given date in database. Request **must** contain following header:
```json
X-API-KEY: $header_value
```  
## Requirements
If one wants to run development version, following tools are required:
- Docker
- Docker-compose
- Makefile 

## Development  
In order to run development server `.env` file is required. Examle file can be found on this repo- `.env.example`. After cloning repo `.env` file should be placed in the root folder of project. To build docker images, in root folder, execute:
```bash
make build-dev
```  
To set conteiners up execute:
```bash
make run-dev
```  
After setting server up there may be need to apply **migrations**. **Migrations** are **OBLIGATORY** to apply if running app first time or if there was any change in the database (don't forget to execute `makemigrations` when introducing changes). To apply migrations:
```bash
make migrate
```

Now local server should be accesible at [0.0.0.0:8000](0.0.0.0:8000), exposing endpoints as described in [Endpoints](#Endpoints) section.