## Endpoints

+ api-token-auth/ - вход
+ api/
    + v1/
        + users/ - users list and user create (login not required)
            + methods: GET, POST
        + users/{id}/ - user detail (ReadOnly for unauthorized)
            + methods: GET, PUT, PATCH, DELETE