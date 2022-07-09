module.exports = {
  title: "Mentorship-Backend",
  tagline: "Documentation for Mentorship Backend",
  url: "https://anitab-org.github.io",
  baseUrl: "/mentorship-backend/",
  onBrokenLinks: "throw",
  favicon: "img/favicon.png",
  organizationName: "anitab-org",
  projectName: "mentorship-backend",
  themeConfig: {
    announcementBar: {
      id: 'support_us',
      content:
        '⭐️ If you like Mentorship-Backend, give it a star on <a href="https://github.com/anitab-org/mentorship-backend" rel="noopener noreferrer" target="_blank">GitHub!</a> ⭐️',
      backgroundColor: '#fafbfc',
      textColor: '#091E42',
    },
    colorMode: {
      defaultMode: "light",
    },
    navbar: {
      title: "Mentorship-Backend Docs",
      hideOnScroll: true,
      logo: {
        alt: "AnitaB.org Logo",
        src: "img/logo.png",
      },
      items: [
        {
          href: "https://anitab.org/",
          label: "AnitaB.org",
          position: "right",
        },
        {
          href: "https://anitab-org.zulipchat.com/#narrow/stream/222534-mentorship-system",
          label: "Zulip",
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
      copyright: `
        <div>
          <a href="https://www.facebook.com/AnitaB.0rg/" rel="noopener noreferrer" target="_blank"><i id="social-fb" class="fa-brands fa-facebook-square fa-3x social"></i></a>
          <a href="https://twitter.com/anitab_org" rel="noopener noreferrer" target="_blank"><i id="social-tw" class="fa-brands fa-twitter-square fa-3x social"></i></a>
          <a href="https://www.linkedin.com/company/anitab-org/" rel="noopener noreferrer" target="_blank"><i id="fa fa-linkedin fa-3x social" class="fa-brands fa-linkedin fa-3x social"></i></a>
          <a href="https://www.instagram.com/anitab_org/" rel="noopener noreferrer" target="_blank"><i id="fa fa-instagram-square fa-2x social" class="fa-brands fa-instagram-square fa-3x social"></i></a>
          <a href="https://medium.com/anitab-org-open-source" rel="noopener noreferrer" target="_blank"><i id="fa fa-medium" class="fa-brands fa-medium fa-3x social"></i></a>
          <a href="https://github.com/anitab-org/mentorship-backend" rel="noopener noreferrer" target="_blank"><i id="fa-brands fa-github" class="fa-brands fa-github fa-3x social"></i></a>
        </div>
        <b>Copyright © ${new Date().getFullYear()} AnitaB.org</b>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
      `,
    },
  },
  presets: [
    [
      "@docusaurus/preset-classic",
      {
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
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
