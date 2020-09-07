module.exports = {
  title: "Mentorship-Backend",
  tagline: "Minimal scaffold for Docusaurus",
  url: "https://your-docusaurus-test-site.com",
  baseUrl: "/",
  onBrokenLinks: "throw",
  favicon: "img/favicon.ico",
  organizationName: "anitab-org", // Usually your GitHub org/user name.
  projectName: "mentorship-backend", // Usually your repo name.
  themeConfig: {
    colorMode: {
      defaultMode: "light",
    },
    navbar: {
      title: "Mentorship-Backend Docs",
      logo: {
        alt: "My Site Logo",
        src: "https://anitab.org/wp-content/uploads/2020/07/logo@2x-300x102.png",
      },
      items: [
        {
          href: "https://anitab.org/",
          label: "AnitaB.org",
          position: "right",
        },
        {
          href: "https://github.com/anitab-org/mentorship-backend",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      copyright: `Copyright © ${new Date().getFullYear()} AnitaB. Built with Docusaurus.`,
    },
  },
  presets: [
    [
      "@docusaurus/preset-classic",
      {
        docs: {
          routeBasePath: "/",
          // It is recommended to set document id as docs home page (`docs/` path).
          homePageId: "home",
          sidebarPath: require.resolve("./sidebars.js"),
          // Please change this to your repo.
          editUrl:
            "https://github.com/anitab-org/mentorship-backend/tree/develop/docs",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      },
    ],
  ],
};
