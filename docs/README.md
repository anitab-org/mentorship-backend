# Mentorship-Backend Docs

This website is built using [Docusaurus 2](https://v2.docusaurus.io/), a modern static website generator.

### Installation

Using `yarn`

```
$ yarn
```
Using `npm`

```
$ npm install
```

### Local Development

Using `yarn`

```
$ yarn start
```

Using `npm`

```
$ npm start
```

This command starts a local development server and open up a browser window. Most changes are reflected live without having to restart the server.

### Build

Using `yarn`

```
$ yarn build
```

Using `npm`

```
$ npm run build
```

### Serve Build

Using `yarn`

```
$ yarn serve
```

Using `npm`

```
$ npm run serve
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

```
$ GIT_USER=<Your GitHub username> USE_SSH=true yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.

## Deploying to Surge

Surge is a static web hosting platform. Tt is used to deploy our spen source programs docusaurus from the command line in a minute.

Deploy using surge with the following steps:

1. Install Surge using npm by running the following command:
    ```
    npm install --g surge
    ```
2. To build the static files of the site for production in the root/docs directory of project, run:
    ```
    npm run build
    ```
3. Run this command inside the root/docs directory of project:
    ```
    surge build/
    ```
    or

    Deploy the site to existing domain using the command:
    ```
    surge build/ https://mentorship-backend.surge.sh
    ```

First-time users of Surge would be prompted to create an account from the command line (happens only once).

Confirm that the site you want to publish is in the build directory, a randomly generated subdomain *.surge.sh subdomain is always given (which can be edited).
