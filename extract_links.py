import re
import os

# Regex for HTML <a> tags: extracts href attribute
html_link_regex = re.compile(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"[^>]*>')

# Regex for Markdown links: extracts URL from [text](URL)
markdown_link_regex = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

# Regex for Astro <Image> and astro:assets Image components
astro_image_regex = re.compile(r'<Image[^>]+src=["\']([^"\']+)["\'][^>]*/>')
astro_assets_image_regex = re.compile(r'import\s+\{\s*Image\s*\}\s+from\s+["\']astro:assets["\'];.*?src:\s*["\']([^"\']+)["\']', re.DOTALL)


# List of files and their content (replace with actual output from read_files)
files_content = [
    {"path": "src/components/BaseHead.astro", "content": """---
interface Props {
  title?: string;
  description?: string;
  image?: string;
}

import { metaData } from "../config";
import { SEO } from "astro-seo";

import { getImagePath } from "astro-opengraph-images";

const { title, description = metaData.description, image } = Astro.props;

const { url, site } = Astro;
const openGraphImageUrl = getImagePath({ url, site });

// If the image is not provided, use the default image
const openGraphImage = image
  ? new URL(image, url.href).href
  : openGraphImageUrl;
---

<SEO
  title={title}
  titleTemplate=`%s | ${metaData.title}`
  titleDefault={metaData.title}
  description={description}
  charset="UTF-8"
  openGraph={{
    basic: {
      title: title || metaData.title,
      type: "website",
      image: openGraphImageUrl,
      url: url,
    },
    optional: {
      description,
      siteName: "Francesco Del Prato",
      locale: "en_US",
    },
  }}
  twitter={{
    card: "summary_large_image",
    title: title || metaData.title,
    description,
    image: openGraphImage,
    creator: "@fdelprato",
  }}
  extend={{
    // extending the default link tags
    link: [{ rel: "icon", href: "/favicon.ico" }],
  }}
/>"""},
    {"path": "src/components/Footer.astro", "content": """---
import { metaData, socialLinks } from "../config";
import { Icon } from "astro-icon/components";

const YEAR = new Date().getFullYear();

const socialIcons = [
  { href: socialLinks.twitter, icon: "fa6-brands:x-twitter" },
  { href: socialLinks.linkedin, icon: "fa6-brands:linkedin-in" },
  { href: socialLinks.email, icon: "tabler:mail-filled" },
];
---

<small class="block lg:mt-24 mt-16 text-[#1C1C1C] dark:text-[#D4D4D4]">
  <time>© {YEAR}</time>{" "}
  <a
    class="no-underline"
    href={socialLinks.twitter}
    target="_blank"
    rel="noopener noreferrer">
    {metaData.title}
  </a>
  <div
    class="flex text-lg gap-3.5 float-right transition-opacity duration-300 hover:opacity-90">
    {
      socialIcons.map((link) => (
        <a href={link.href} target="_blank" rel="noopener noreferrer">
          <Icon name={link.icon} />
        </a>
      ))
    }
    <a href="/rss.xml" target="_self">
      <Icon name="fa6-solid:rss" />
    </a>
  </div>
</small>

<style>
  @media screen and (max-width: 480px) {
    article {
      padding-top: 2rem;
      padding-bottom: 4rem;
    }
  }
</style>"""},
    {"path": "src/components/FormattedDate.astro", "content": """---
interface Props {
  date: Date | string;
  includeRelative?: boolean;
}

const { date, includeRelative = false } = Astro.props;

const formatDate = (date: Date | string, includeRelative: boolean): string => {
  let currentDate = new Date();
  let targetDate = date instanceof Date ? date : new Date(date);

  if (isNaN(targetDate.getTime())) {
    console.error("Invalid date:", date);
    return "Invalid Date";
  }

  let yearsAgo = currentDate.getFullYear() - targetDate.getFullYear();
  let monthsAgo = currentDate.getMonth() - targetDate.getMonth();
  let daysAgo = currentDate.getDate() - targetDate.getDate();

  let formattedDate = "";

  if (yearsAgo > 0) {
    formattedDate = `${yearsAgo}y ago`;
  } else if (monthsAgo > 0) {
    formattedDate = `${monthsAgo}mo ago`;
  } else if (daysAgo > 0) {
    formattedDate = `${daysAgo}d ago`;
  } else {
    formattedDate = "Today";
  }

  let fullDate = targetDate.toLocaleString("en-us", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });

  if (!includeRelative) {
    return fullDate;
  }

  return `${fullDate} (${formattedDate})`;
};

const formattedDateString = formatDate(date, includeRelative);
---

<time datetime={new Date(date).toISOString()}>
  {formattedDateString}
</time>"""},
    {"path": "src/components/Nav.astro", "content": """---
import { metaData } from "../config";
import { Icon } from "astro-icon/components";

const navItems = {
  "/research": { name: "Research" },
  "/teaching": { name: "Teaching" },
  "/op-eds":   { name: "Op-eds"  },
  "/DelPrato_CV.pdf" : { name : "CV" },
};
---

<nav class="lg:mb-16 mb-12 py-5">
  <div class="flex flex-col md:flex-row md:items-center justify-between">
    <div class="flex items-center">
      <a href="/" class="text-3xl font-semibold">
        {metaData.title}
      </a>
    </div>
    <div class="flex flex-row gap-4 mt-6 md:mt-0 md:ml-auto items-center">
      {
        Object.entries(navItems).map(([path, { name }]) => (
          <a
            href={path}
            class="transition-all hover:text-neutral-800 dark:hover:text-neutral-200 flex align-middle relative">
            {name}
          </a>
        ))
      }
      <button
        id="theme-toggle"
        aria-label="Toggle theme"
        class="flex items-center justify-center transition-opacity duration-300 hover:opacity-90">
        <Icon
          name="fa6-solid:circle-half-stroke"
          class="h-[14px] w-[14px] text-[#1c1c1c] dark:text-[#D4D4D4]"
        />
      </button>
    </div>
  </div>
</nav>

<script is:inline>
  function setTheme(theme) {
    document.dispatchEvent(new CustomEvent("set-theme", { detail: theme }));
  }

  function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";
    setTheme(newTheme);
  }

  document.addEventListener("astro:page-load", () => {
    document
      .getElementById("theme-toggle")
      .addEventListener("click", toggleTheme);
  });
</script>"""},
    {"path": "src/components/mdx/Callout.astro", "content": """---
interface Props {
  emoji: string;
}

const { emoji } = Astro.props;
---

<div
  class="px-4 py-3 bg-[#F7F7F7] dark:bg-[#181818] rounded p-1 text-sm flex items-center text-neutral-900 dark:text-neutral-100 mb-8">
  <div class="flex items-center w-4 mr-4">{emoji}</div>
  <div class="w-full callout leading-relaxed">
    <slot />
  </div>
</div>"""},
    {"path": "src/components/mdx/Caption.astro", "content": """---
import { Balancer } from "react-wrap-balancer";
---

<span
  class="block w-full text-xs my-3 font-mono text-gray-500 text-center leading-normal">
  <Balancer>
    <span class="">
      <slot />
    </span>
  </Balancer>
</span>"""},
    {"path": "src/components/mdx/ImageGrid.astro", "content": """---
import { Image } from "astro:assets";

interface ImageGridProps {
  images: {
    src: string;
    alt: string;
    href?: string;
  }[];
  columns?: 2 | 3 | 4;
}

const { images, columns = 3 } = Astro.props as ImageGridProps;

const gridClass = {
  2: "grid-cols-2 sm:grid-cols-2",
  3: "grid-cols-2 sm:grid-cols-3",
  4: "grid-cols-2 sm:grid-cols-4",
}[columns];
---

<section>
  <div class={`grid ${gridClass} gap-4 my-8`}>
    {
      images.map((image) => (
        <div class="relative aspect-square">
          {image.href ? (
            <a
              target="_blank"
              rel="noopener noreferrer"
              href={image.href}
              class="block w-full h-full">
              <Image
                alt={image.alt}
                src={image.src}
                width={500}
                height={500}
                class="rounded-lg object-cover w-full h-full"
              />
            </a>
          ) : (
            <Image
              alt={image.alt}
              src={image.src}
              width={500}
              height={500}
              class="rounded-lg object-cover w-full h-full"
            />
          )}
        </div>
      ))
    }
  </div>
</section>"""},
    {"path": "src/components/mdx/Table.astro", "content": """---
interface TableData {
  headers: string[];
  rows: string[][];
}

interface Props {
  data: TableData;
}

const { data } = Astro.props;
---

<table>
  <thead>
    <tr class="text-left">
      {data.headers.map((header) => <th>{header}</th>)}
    </tr>
  </thead>
  <tbody>
    {
      data.rows.map((row) => (
        <tr>
          {row.map((cell) => (
            <td>{cell}</td>
          ))}
        </tr>
      ))
    }
  </tbody>
</table>"""},
    {"path": "src/components/mdx/Tweet.astro", "content": """---
import { getTweet } from "react-tweet/api";
import { EmbeddedTweet, TweetNotFound, type TweetProps } from "react-tweet";
import "./tweet.css";

interface Props {
  id: string;
}

const { id } = Astro.props;

let tweet;
let error;

if (id) {
  try {
    tweet = await getTweet(id);
  } catch (err) {
    console.error(err);
    error = err;
  }
}

const TweetContent = () => {
  if (!tweet) {
    return <TweetNotFound error={error} />;
  }
  return <EmbeddedTweet tweet={tweet} />;
};
---

<div class="tweet my-6">
  <div class="flex justify-center">
    <TweetContent />
  </div>
</div>"""},
    {"path": "src/components/mdx/YouTube.astro", "content": """---
import YT from "react-youtube";

interface Props {
  videoId: string;
}

const { videoId } = Astro.props;
---

<div class="relative w-full h-0 pb-[56.25%] my-6">
  <YT
    opts={{
      height: "100%",
      width: "100%",
    }}
    videoId={videoId}
    class="absolute top-0 left-0 w-full h-full"
  />
</div>"""},
    {"path": "src/content/blog/custom-mdx-examples.mdx", "content": """---
title: "Custom MDX Examples"
publishedAt: "2024-08-11"
summary: "Astrofolio custom MDX examples."
tags: "Custom MDX, Web development"
---
import { Image } from "astro:assets";
import Tweet from "astro-tweet";
import { YouTube } from '@astro-community/astro-embed-youtube';
import ImageGrid from "../../components/mdx/ImageGrid.astro";
import Caption from "../../components/mdx/Caption.astro";
import Table from "../../components/mdx/Table.astro";
import Callout from "../../components/mdx/Callout.astro";

Astrofolio uses [custom MDX](https://github.com/vikas5914/Astrofolio/blob/main/src/components/mdx) for blog posts, making it easy to include JSX components such as interactive embeds, charts, or alerts directly in your markdown content.

Here are some examples of using MDX:

## h2 Heading

### h3 Heading

#### h4 Heading

##### h5 Heading

## Emphasis

**This is bold text**

_This is italic text_

<del> Strikethrough </del>

## Blockquotes

> If today were the last day of my life, would I want to do what I am about to do today? – Steve Jobs

## Links

- Astrofolio is built with [Astro](https://astro.build/).
- Astrofolio uses [bun](https://bun.sh/) for package management.

## CodeBlocks

```jsx
// This is commented-out code
export default function HelloWorld() {
  return (
    <h1>Hello, World!</h1>
  );
}
```

## Images

Astrofolio uses [Astro Image](https://docs.astro.build/en/guides/images/) in MDX for seamless image rendering:

```jsx
<Image
  src="/opengraph-image.png"
  alt="OpenGraph image"
  width={640}
  height={500}
/>
```

Renders:

<Image
  src="/opengraph-image.png"
  alt="OpenGraph image"
  width={640}
  height={500}
/>

## Image Grid

Astrofolio uses a custom [image grid component](https://github.com/vikas5914/Astrofolio/blob/main/src/components/mdx/ImageGrid.astro) to display image galleries.

```jsx
<ImageGrid
  columns={3} // Accepts 2, 3, or 4 columns
  images={[
    { src: "/photos/photo1.jpg", alt: "Photo1", href: "#" }, // 'href' is optional
    { src: "/photos/photo2.jpg", alt: "Photo2", href: "#" },
    { src: "/photos/photo3.jpg", alt: "Photo3"},
  ]}
/>
```

Renders:

<ImageGrid
  columns={3}
  images={[
    { src: "/photos/photo1.jpg", alt: "Photo1", href: "#" },
    { src: "/photos/photo2.jpg", alt: "Photo2", href: "#" },
    { src: "/photos/photo3.jpg", alt: "Photo3" },
  ]}
/>

## Embeds

### Tweets

Astrofolio uses [astro-tweet](https://github.com/tsriram/astro-tweet/) to embed tweets in MDX posts.

```jsx
<Tweet id="1617979122625712128" />
```

Renders:

<div className="tweet">
  <div className={`flex justify-center`}>
    <Tweet id="1617979122625712128" />
  </div>
</div>


### YouTube Videos

Astrofolio uses [astro-embed](https://astro-embed.netlify.app/) to embed YouTube videos in MDX posts.

```jsx
<YouTube id="wXhTHyIgQ_U" />
```

Renders:

<YouTube id="wXhTHyIgQ_U" />

### Captions

Astrofolio uses [react-wrap-balancer](https://react-wrap-balancer.vercel.app/) to evenly balance captions in MDX posts.

```jsx
<Caption>
  Captions that flow smoothly, making your content easy to read and visually
  appealing with a clean look.
</Caption>
```

Renders:

<Caption>
  Captions that flow smoothly, making your content easy to read and visually
  appealing with a clean look.
</Caption>

## Tables

Astrofolio uses a custom [table component](https://github.com/vikas5914/Astrofolio/blob/main/src/components/mdx/Table.astro) to render tables in MDX posts.

```jsx
<Table
  data={{
    headers: ["Title", "Description"],
    rows: [
      [
        "First item",
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Aliquid perspiciatis repellat amet quos.",
      ],
      [
        "Second item",
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Aliquid perspiciatis repellat amet quos.",
      ],
    ],
  }}
/>
```

Renders:

<Table
  data={{
    headers: ["Title", "Description"],
    rows: [
      [
        "First item",
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Aliquid perspiciatis repellat amet quos.",
      ],
      [
        "Second item",
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Aliquid perspiciatis repellat amet quos.",
      ],
    ],
  }}
/>

## Math Expressions

Astrofolio allows you to render mathematical expressions in MDX posts using [KaTeX](https://katex.org/) . Simply wrap your expression in **$** to include KaTeX within your MDX content.

```
$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$
```

Renders:

$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$

## Callout

Astrofolio uses a custom [callout component](https://github.com/vikas5914/Astrofolio/blob/main/src/components/mdx/Callout.astro) to render important information in MDX posts.

```jsx
<Callout emoji="💡">
  [Astrofolio](https://astrofolio-astro.vercel.app/) is a clean, simple, and fast portfolio built with Astro, Tailwind CSS, and bun for optimal performance.
</Callout>
```

Renders:

<Callout emoji="💡">
  [Astrofolio](https://astrofolio-astro.vercel.app/) is a clean, simple, and fast portfolio built with Astro, Tailwind CSS, and bun for optimal performance.
</Callout>"""},
    {"path": "src/content/blog/getting-started.mdx", "content": """---
title: "Getting Started with Astrofolio"
publishedAt: "2024-08-13"
summary: "Instructions to build and configure your Astrofolio portfolio."
tags: "Configuration, Web development"
---

Astrofolio includes all the essentials for a stunning portfolio website.

Start by [deploying](https://vercel.com/new/clone?repository-url=https://github.com/vikas5914/Astrofolio) your portfolio with Vercel in minutes, or fork the [repository](https://github.com/vikas5914/Astrofolio) and follow the instructions below to set it up.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/vikas5914/Astrofolio)

## Installation

Astrofolio uses [bun](https://bun.sh) for dependency management, so ensure it is installed on your system.

Clone the repository and run the following command to install the dependencies:

```jsx
git clone https://github.com/vikas5914/Astrofolio
cd Astrofolio
bun i
```

Start the development server:

```jsx
bun dev
```

The server will be running at [http://localhost:4321/](http://localhost:4321/).

## Configuration

Customize your Astrofolio setup by updating your information to ensure proper SEO, feed generation, Open Graph integration, and other settings.

### Config.ts

Update the site metadata and social links in the **src/config.js** file. These constants are utilized across the site for SEO, feeds, social links, and Open Graph integration.

```jsx
export const metaData = {
  baseUrl: "https://astrofolio-astro.vercel.app/",
  title: "Astrofolio",
  name: "Vikas",
  ogImage: "/opengraph-image.png",
  description:
    "A clean, fast, and lightweight portfolio template built with Next.js, Vercel, and Tailwind CSS for optimal performance.",
};

export const socialLinks = {
  twitter: "https://x.com/vikas5914",
  github: "https://github.com/vikas5914/Astrofolio",
  instagram: "https://www.instagram.com/",
  linkedin: "https://www.linkedin.com/",
  email: "mailto:example@gmail.com",
};

```

### Sitemap

With Astro Sitemap, you don’t have to worry about creating this XML file yourself: the Astro Sitemap integration will crawl your statically-generated routes and create the sitemap file.

### Profile Photo

Update your profile photo by replacing the **public/profile.png** file with your image.

### Favicon

Update your favicon by replacing the **public/favicon.ico** file with your custom icon.

## Analytics

Astrofolio uses [Vercel Web Analytics](https://vercel.com/docs/analytics/quickstart) to monitor user interactions. Simply deploy your site on Vercel and enable feature through the Vercel dashboard.

## Ready!

You're all set! Update your blog posts in the **/content** folder, add your project data in **pages/projects/index.astro**, and update your images in **pages/photos/index.astro**.

Your portfolio is equipped with SEO and [RSS](/rss.xml), as well as analytics. Astrofolio is fully customizable, allowing you to add features as needed."""},
    {"path": "src/layouts/Base.astro", "content": """---
interface Props {
  title?: string;
  description?: string;
  image?: string;
}

import Themes from "astro-themes";
import { ViewTransitions } from "astro:transitions";

import BaseHead from "../components/BaseHead.astro";
import Navbar from "../components/Nav.astro";
import Footer from "../components/Footer.astro";

import "@fontsource/geist-sans/400.css";
import "@fontsource/geist-sans/600.css";
import "@fontsource/geist-mono/400.css";
import "@fontsource/geist-mono/600.css";
import "@styles/global.css";

const { title, description, image } = Astro.props;
---

<html lang="en" class="scrollbar-hide lenis lenis-smooth">
  <head>
	
<!-- Google tag (gtag.js) -->
<script
  is:inline
  type="text/partytown"
  src="https://www.googletagmanager.com/gtag/js?id=G-CB0P1912PV"
></script>

<script is:inline type="text/partytown">
  window.dataLayer = window.dataLayer || [];
  function gtag() {
    dataLayer.push(arguments);
  }
  gtag("js", new Date());

  gtag("config", "G-CB0P1912PV");
</script>


    <ViewTransitions />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta
      name="googlebot"
      content="index, follow, max-video-preview:-1, max-image-preview:large, max-snippet:-1"
    />
    <link rel="sitemap" href="/sitemap-index.xml" />
    <Themes />
    <BaseHead title={title} description={description} image={image} />
    <link
      rel="alternate"
      type="application/rss+xml"
      title="Francesco Del Prato"
      href={new URL("rss.xml", Astro.site)}
    />
    <script>
      import "@scripts/lenisSmoothScroll.js";
    </script>
  </head>
  <body
    class="antialiased flex flex-col items-center justify-center mx-auto mt-2 lg:mt-8 mb-20 lg:mb-40
    scrollbar-hide">
    <main
      class="flex-auto min-w-0 mt-2 md:mt-6 flex flex-col px-6 sm:px-4 md:px-0 max-w-[640px] w-full">
      <Navbar />
      <slot />
      <Footer />
    </main>
    <style>
      /* CSS rules for the page scrollbar */
      .scrollbar-hide::-webkit-scrollbar {
        display: none;
      }

      .scrollbar-hide {
        -ms-overflow-style: none;
        scrollbar-width: none;
      }
    </style>
  </body>
</html>"""},
    {"path": "src/pages/blog/[...slug].astro", "content": """---
import { type CollectionEntry, getCollection } from "astro:content";
import Base from "../../layouts/Base.astro";
import FormattedDate from "../../components/FormattedDate.astro";
import "katex/dist/katex.min.css";
import { metaData } from "../../config";

export async function getStaticPaths() {
  const posts = await getCollection("blog");
  return posts.map((post) => ({
    params: { slug: post.slug },
    props: post,
  }));
}
type Props = CollectionEntry<"blog">;

import { getImagePath } from "astro-opengraph-images";
const post = Astro.props;
const { url, site } = Astro;
const openGraphImageUrl = getImagePath({ url, site });

const { Content } = await post.render();
---

<Base title={post.data.title} description={post.data.summary}>
  <section>
    <script
      type="application/ld+json"
      set:html={JSON.stringify({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        headline: post.data.title,
        datePublished: post.data.publishedAt,
        dateModified: post.data.publishedAt,
        description: post.data.summary,
        image: openGraphImageUrl,
        url: url,
        author: {
          "@type": "Person",
          name: metaData.name,
        },
      })}
    />
    <h1 class="title mb-3 font-medium text-2xl tracking-tight">
      {post.data.title}
    </h1>
    <div class="flex justify-between items-center mt-2 mb-8 text-medium">
      <p class="text-sm text-neutral-600 dark:text-neutral-400">
        <FormattedDate date={post.data.publishedAt} includeRelative={false} />
      </p>
    </div>
    <article class="prose prose-quoteless prose-neutral dark:prose-invert">
      <Content />
    </article>
  </section>
</Base>"""},
    {"path": "src/pages/blog/index.astro", "content": """---
import Base from "../../layouts/Base.astro";
import { getCollection } from "astro:content";
import FormattedDate from "../../components/FormattedDate.astro";

const posts = (await getCollection("blog")).sort(
  (a, b) => b.data.publishedAt.valueOf() - a.data.publishedAt.valueOf()
);

const title = "Blog";
const description = "Astrofolio Blog";
---

<Base title={title} description={description}>
  <section>
    <h1 class="mb-8 text-2xl font-medium tracking-tight">Our Blog</h1>
    <div>
      {
        posts.map((post) => (
          <a
            class="flex flex-col space-y-1 mb-4 transition-opacity duration-200 hover:opacity-80"
            href={`/blog/${post.slug}`}>
            <div class="w-full flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-1 sm:space-y-0 sm:space-x-2">
              <p class="text-black dark:text-white tracking-tight">
                {post.data.title}
              </p>
              <p class="text-neutral-600 dark:text-neutral-400 tabular-nums text-sm">
                <FormattedDate
                  date={post.data.publishedAt}
                  includeRelative={false}
                />
              </p>
            </div>
          </a>
        ))
      }
    </div>
  </section>
</Base>"""},
    {"path": "src/pages/index.astro", "content": """---
import Base from "../layouts/Base.astro";
import { socialLinks } from "../config";
import { Image } from "astro:assets";
---

<Base>
  <section>
    <a href={socialLinks.twitter} target="_blank">
      <Image
        src={`${import.meta.env.BASE_URL}profile.png`}
        alt="Profile photo"
        class="rounded-full bg-gray-100 block lg:mt-5 mt-0 lg:mb-5 mb-10 mx-auto sm:float-right sm:ml-5 sm:mb-5 grayscale hover:grayscale-0"
        width={160}
        height={160}
      />
    </a>

    <h1 class="mb-2 text-2xl font-medium tracking-tight">
      About me
    </h1>

    <div class="prose prose-neutral dark:prose-invert">
      <p>I am an assistant professor at the Department of Economics and Business Economics at <a href="https://econ.au.dk/">Aarhus University</a>.</p> 
      <p>I am interested in Macro/Labor Economics, particularly the interplay between labor market dynamics and public policy.</p>
      <p>My work usually employs a mix of structural and reduced-form approaches that exploit administrative microdata.</p>
   
      <h1 class="mb-2 text-2xl font-medium tracking-tight">
        Contact
      </h1>
      <p>
        Department of Economics and Business Economics <br>
        Aarhus BSS, Aarhus University <br>
        Fuglesangs Allé 4, bld. 2632 <br>
        8210 Aarhus V, Denmark
      </p>
    </div>
  </section>
</Base>"""},
    {"path": "src/pages/op-eds/index.astro", "content": """---
import Base from "../../layouts/Base.astro";

const opEds = [
  {
    title: "Le criticità di un salario minimo a 9 euro nel contesto Italiano",
    publication: "Il Foglio",
    date: "17 giugno 2022",
    coauthor: "Matteo Paradisi",
    pdf: "/opeds/salariominimo_foglio_22.pdf",
    digital: "https://www.ilfoglio.it/economia/2022/06/17/news/le-criticita-di-un-salario-minimo-a-9-euro-nel-contesto-italiano--4126922/"
  },
  {
    title: "Alireza ha scelto",
    publication: "Il Foglio",
    date: "26 gennaio 2022",
    coauthor: "Cecilia Sala",
    digital: "https://www.ilfoglio.it/cultura/2022/01/29/news/preferisci-l-iran-o-vincere-alireza-ha-scelto-3589459/"
  },
  {
    title: "Una bolla per le RSA",
    publication: "Il Foglio",
    date: "29 ottobre 2020",
    coauthor: "Gianluca Rinaldi",
    pdf: "/opeds/rsa_foglio.pdf",
    digital: "https://www.ilfoglio.it/salute/2020/10/29/news/una-bolla-anti-covid-per-le-rsa-1322600/"
  },
  {
    title: "L’unico vero antidoto a Quota 100 si chiama Ape Volontario",
    publication: "Il Foglio",
    date: "2 gennaio 2020",
    coauthor: "Matteo Paradisi",
    pdf: "/opeds/ape_foglio.pdf",
    digital: "https://www.ilfoglio.it/economia/2020/01/02/news/lunico-vero-antidoto-a-quota-100-si-chiama-ape-volontario-294615/"
  },
  {
    title: "Tutte le tasse di Fioramonti, tra inefficacia e iniquità",
    publication: "Il Foglio",
    date: "27 settembre 2019",
    coauthor: "Matteo Paradisi",
    pdf: "/opeds/sugar_tax_foglio.pdf",
    digital: "https://www.ilfoglio.it/economia/2019/09/26/news/tutte-le-tasse-di-fioramonti-tra-inefficacia-e-iniquita-276660/"
  },
  {
    title: "In Italia il salario minimo serve solo alla politica",
    publication: "Il Foglio",
    date: "04 settembre 2019",
    coauthor: "Matteo Paradisi",
    pdf: "/opeds/salario_minimo_foglio.pdf",
    digital: "https://www.ilfoglio.it/economia/2019/09/04/news/in-italia-il-salario-minimo-universale-serve-solo-alla-politica-272279/"
  }
];


const title = "Op-eds";
const description = "A collection of newspaper publications by Francesco.";
---

<Base title={title} description={description}>

<section>
  <h2 class="text-2xl font-medium mb-6">Op-eds in Italian Newspapers</h2>
  <div class="space-y-4">
    {opEds.map((opEd, index) => (
      <div key={index} class="flex flex-col space-y-1">
        <div class="flex justify-between items-baseline">
          <span class="text-black dark:text-white tracking-tight font-bold">
            {opEd.title}
          </span>

          <div class="text-neutral-600 dark:text-neutral-400 tabular-nums text-sm flex items-center space-x-2">
            {opEd.pdf && (
              <a
                href={opEd.pdf}
                target="_blank"
                rel="noopener noreferrer"
                class="hover:underline"
              >
                pdf
              </a>
            )}
            {opEd.pdf && opEd.digital && <span>|</span>}
            {opEd.digital && (
              <a
                href={opEd.digital}
                target="_blank"
                rel="noopener noreferrer"
                class="hover:underline"
              >
                digital
              </a>
            )}
          </div>
        </div>

        <p class="text-sm text-neutral-600 dark:text-neutral-400">
          {opEd.publication}, {opEd.date}
          {opEd.coauthor && `, con ${opEd.coauthor}`}
        </p>
      </div>
    ))}
  </div>
</section>


</Base>"""},
    {"path": "src/pages/research/index.astro", "content": """---
import Base from "../../layouts/Base.astro";

const wp = [

  {
    title: "Workers as Partners: a Theory of Responsible Firms in Labor Markets",
    coauthors: [{ name: "Marc Fleurbaey", url: "https://sites.google.com/site/marcfleurbaey/Home" }],
    description:
      "We develop a theoretical framework analyzing responsible firms (REFs) that prioritize worker welfare alongside profits in labor markets with search frictions. At the micro level, REFs’ use of market power varies with labor conditions: they refrain from using it in slack markets but may exercise it in tight markets without harming workers. Our macro analysis shows these firms offer higher wages, creating a distinct high-wage sector. When firms endogenously choose worker bargaining power, there is trade-off between worker surplus and employment, though this improves with elastic labor supply. While REFs cannot survive with free entry, they can coexist with profit-maximizing firms under limited competition, where their presence forces ordinary firms to raise wages.",
    pdf: "/RF_theory.pdf",
    arxiv: "https://arxiv.org/abs/2411.05567",
  },

  {
    title: "The Importance of Working for Earnest: Climbing the Job Ladder through Firms’ Connectivity",
    notes: "> Project selected for the VisitINPS 2019 program",
    description:
      "Do workers consider a firm’s “springboard” value in terms of future job opportunities when choosing an employer? Using a search model of the labor market, I introduce the idea that firms differ in enhancing their employees’ chances of receiving external job offers. The model informs a firm-level proxy for outside job offers received by workers. This measure empirically aligns with key model predictions: 1) it negatively correlates with both firm-specific tenure and young workers’ entry salaries, revealing a compensating differential; and 2) it suggests that workers enjoy a salary premium upon leaving such firms, indicative of faster career progression. The model is estimated on administrative data from Italy and successfully captures key aspects of labor market dynamics. My channel explains 10% of the overall job-to-job transitions and shows how firm-induced variation in job search can be a significant driver of inequality, especially at the bottom of the wage distribution.",
    pdf: "/JMP_DelPrato.pdf",
  },

    {
    title: "Frictions and Welfare in Monopolistic Competition",
    coauthors: [{ name: "Paolo Zacchia", url: "http://paolozacchia.com" }],
    description:
      "We study informational financial frictions in heterogeneous firm economies with monopolistic competition. We extend the Melitz model by introducing banks that finance entrepreneurs under asymmetric information. While aggregate productivity decreases with information frictions, welfare can be maximized at intermediate levels of asymmetry due to a trade-off between productivity and product variety. Furthermore, moderate input cost distortions can improve welfare when financial frictions are severe by offsetting the resulting weak firm selection.",
    pdf: "/iff.pdf",
  },

  {
    title: "The Heterogeneous Consequences of Reduced Labor Costs on Firm Productivity",
    coauthors: [{ name: "Paolo Zacchia", url: "http://paolozacchia.com" }],
    notes: "> New version coming soon! | Project selected for the VisitINPS 2020 program",
    description:
      "We document how a reduction in labor costs led to heterogeneous effects on manufacturing firms’ total factor productivity (TFP). Leveraging an Italian labor legislation reform and unique institutional features of the local collective bargaining system, we show that such effects vary along the TFP distribution. Relative to the counterfactual, TFP markedly declines on the left tail, which we explain via selection mechanisms; on the right, TFP mildly increases as firms are able to expand and reallocate their workforce. We develop a general equilibrium model featuring firm selection and frictions in input markets to guide the evaluation of welfare implications.",
  },

  {
    title: "Optimal Ramsey Taxation with Social Security",
    coauthors: [
      { name: "Marco Francischello", url: "https://marcofrancis.me" },
      { name: "Matteo Paradisi", url: "http://matteoparadisi.com" }
    ],
    notes: "> Project awarded with a Netspar Comparative Research Grant 2021",  
    description:
      "We develop an OLG model with heterogeneous agents and aggregate uncertainty to study optimal Ramsey taxation when the government can use a credible set of social security instruments. Social security mitigates the income effect in optimal labor tax smoothing and, together with heterogeneity, adds new redistributive motives to both labor and capital taxes while crowding out others. We calibrate the model on three different economies: the US, Netherlands, and Italy. We argue that the three countries would experience heterogeneous gains, in redistributive and efficiency terms, by moving from the status-quo allocations to those prescribed by a utilitarian Ramsey planner. Our simulations show that retirement benefits in the current economies are higher than their Ramsey-optimal level while we argue that the use of funded social security schemes, neglected in current actual policies, could be welfare improving.",
    pdf: "/ot_retirement_paper.pdf",
  },


];


const wip = [

  {
    title: "Responsible Firms on the Labor Market",
    coauthors: [{ name: "Marc Fleurbaey", url: "https://sites.google.com/site/marcfleurbaey/Home" }],
    notes: "Project selected for the VisitINPS 2023 program",
    description: 
	"Responsible firms prioritize maximizing stakeholder value, which entails balancing the surpluses of their customers and workers along with their profits. In this paper, we focus on firms' behavior within the labor market and introduce a theory-backed method for identifying responsible firms using administrative data. By integrating measures of labor market power and systematic utility provided to workers, we construct a multi-dimensional index of responsibility. This enables us to categorize companies and assess the degree of a firm's responsibility throughout its life cycle. Furthermore, we evaluate the influence of a firm's responsibility on income inequalities both within and between firms.",
  },

  {
    title: "Human Capital Value Chains",
    coauthors: [{ name: "Paolo Zacchia", url: "http://paolozacchia.com" }],
    notes: "Project selected for the VisitINPS 2023 program",
    description: 
	"In local labor markets, a pattern often emerges where workers transition during the early stages of their careers from lower-paying firms that provide comprehensive training to higher-paying specialized firms that predominantly employ already-trained workers. We refer to this mechanism as the “Human Capital Value Chain” (HCVC). We study and document its impact on the trajectory of workers' wages and local agglomeration externalities, thereby highlighting its role in the broader labor market dynamics.",
  },

  {
    title: "Generalized AKM: Theory and Evidence",
    coauthors: [
	{ name: "Yaroslav Korobka" },
	{ name: "Paolo Zacchia", url: "http://paolozacchia.com" }
    ],
    description: 
	"We revisit the wage decomposition literature by allowing for a non-parametric function of both worker- and firm-level covariates in a wage equation with two-way (worker and firm) fixed effects. We develop theoretical results about the estimation of key covariance components and an application on Portuguese data.",
  },

];



const title = "Working Papers and Work in Progress";
const description = "A collection of working papers and work in progress by the author.";
---

<Base title={title} description={description}>
  <section>
    <!-- Working Papers Section -->
    <h1 class="mb-8 text-2xl font-medium tracking-tight">Working Papers</h1>
    <div class="space-y-6">
      {wp.map((project, index) => (
        <div class="flex flex-col" key={index}>
          <div class="w-full flex justify-between items-baseline">
            <span class="text-black dark:text-white tracking-tight font-bold">
              {project.title}
            </span>
            
            <div class="text-neutral-600 dark:text-neutral-400 tabular-nums text-sm ml-2 flex items-center space-x-2">
              {project.pdf && (
                <a
                  href={project.pdf}
                  target="_blank"
                  rel="noopener noreferrer"
                  class="hover:underline"
                >
                  PDF
                </a>
              )}
              {project.pdf && project.arxiv && <span>|</span>}
              {project.arxiv && (
                <a
                  href={project.arxiv}
                  target="_blank"
                  rel="noopener noreferrer"
                  class="hover:underline"
                >
                  ArXiv
                </a>
              )}
            </div>
          </div>
          
          {project.coauthors && (
            <p class="italic">
              Joint with{" "}
              {project.coauthors.map((author, i) => (
                <span key={i}>
                  {author.url ? (
                    <a
                      href={author.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      class="text-blue-500 hover:underline"
                    >
                      {author.name}
                    </a>
                  ) : (
                    author.name
                  )}
                  {i < project.coauthors.length - 2 ? ", " : i === project.coauthors.length - 2 ? " and " : ""}
                </span>
              ))}
            </p>
          )}
          
          {project.notes && (
            <p class="text-neutral-600 dark:text-neutral-400 tabular-nums text-sm">{project.notes}</p>
          )}
          
          <!-- Toggleable Description with Left-Aligned "Show More" Button -->
          <button
            onclick={`document.getElementById('wp-desc-${index}').classList.toggle('hidden')`}
            class="text-neutral-600 dark:text-neutral-400 tabular-nums text-sm flex items-center mt-2"
          >
            <span class="mr-1">▼</span> Abstract
          </button>
          
          <p id={`wp-desc-${index}`} class="prose prose-neutral dark:prose-invert pt-3 hidden">
            {project.description}
          </p>
        </div>
      ))}
    </div>
  </section>

  
  <!-- Work in Progress Section -->
  <h1 class="mb-8 mt-12 text-2xl font-medium tracking-tight">Selected Work in Progress</h1>
  <div class="space-y-6">
    {wip.map((project, index) => (
      <div class="flex flex-col" key={`wip-${index}`}>
        <div class="w-full flex justify-between items-baseline">
          <span class="text-black dark:text-white tracking-tight font-bold">
            {project.title}
          </span>
          {project.year && (
            <span class="text-neutral-600 dark:text-neutral-400 tabular-nums text-sm">
              {project.year}
            </span>
          )}
        </div>

        {project.coauthors && (
          <p class="italic">
            Joint with{" "}
            {project.coauthors.map((author, i) => (
              <span key={i}>
                {author.url ? (
                  <a
                    href={author.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    class="text-blue-500 hover:underline"
                  >
                    {author.name}
                  </a>
                ) : (
                  author.name
                )}
                {i < project.coauthors.length - 2 ? ", " : i === project.coauthors.length - 2 ? " and " : ""}
              </span>
            ))}
          </p>
        )}

        {project.notes && (
          <p class="text-neutral-600 dark:text-neutral-400 tabular-nums text-sm">
            {project.notes}
          </p>
        )}

        <!-- Toggleable Description with Left-Aligned "Show More" Button -->
        <button
          onclick={`document.getElementById('wip-desc-${index}').classList.toggle('hidden')`}
          class="text-neutral-600 dark:text-neutral-400 tabular-nums text-sm flex items-center mt-2"
        >
          <span class="mr-1">▼</span> Short abstract
        </button>

        <p id={`wip-desc-${index}`} class="prose prose-neutral dark:prose-invert pt-3 hidden">
          {project.description}
        </p>
      </div>
    ))}
  </div>
</Base>"""},
    {"path": "src/pages/teaching/index.astro", "content": """---
import Base from "../../layouts/Base.astro";

const teachingExperience = [
  {
    institution: "CERGE-EI",
    course: "Microeconometrics, Ph.D.",
    term: "Fall 2021",
    details: "Lectures on random search models and their estimation through SMM (slides available upon request)"
  },
  {
    institution: "IMT Lucca",
    courses: [
      {
        name: "Econometrics I, Ph.D.",
        term: "Spring 2019, 2020",
        role: "TA for prof. Paolo Zacchia"
      },
      {
        name: "Microeconomics, Ph.D.",
        term: "Fall 2019",
        role: "TA for prof. Andrea Canidio and prof. Kenan Huremovic"
      }
    ]
  },
  {
    institution: "KU Leuven",
    details: "Advising assistant for master students’ theses"
  }
];


const currentTeaching = [
  {
    institution: "Aarhus University",
    course: "5425/6425: Advanced Micro and Macro Models of the Labor Market",
    term: "Spring 2025",
  }
];



const title = "Teaching";
const description = "The teaching of Francesco Del Prato";
---

<Base title={title} description={description}>

<section>
  <h2 class="text-2xl font-medium mb-6">Current Teaching</h2>
  <div class="space-y-4">
    {currentTeaching.map((entry, index) => (
      <div key={index} class="flex flex-col space-y-1">
        <span class="font-bold">{entry.institution}</span>
        <p class="text-sm">
          {entry.course} ({entry.term}) - {entry.details}
        </p>
      </div>
    ))}
  </div>
</section>

<br><br>

<section>
  <h2 class="text-2xl font-medium mb-6">Teaching Experience</h2>
  <div class="space-y-4">
    {teachingExperience.map((entry, index) => (
      <div key={index} class="flex flex-col space-y-1">
        <span class="font-bold">{entry.institution}</span>
        
        {entry.course ? (
          <p class="text-sm">
            {entry.course} ({entry.term}) - {entry.details}
          </p>
        ) : (
          entry.courses && entry.courses.map((course, i) => (
            <p key={i} class="text-sm">
              {course.name} ({course.term}) - {course.role}
            </p>
          ))
        )}

        {entry.details && !entry.course && (
          <p class="text-sm text-neutral-700">{entry.details}</p>
        )}
      </div>
    ))}
  </div>
</section>

   
</Base>"""}
]

all_links = []

for file_data in files_content:
    file_path = file_data["path"]
    content = file_data["content"]

    # Find HTML links
    for match in html_link_regex.finditer(content):
        link_url = match.group(1)
        if link_url.startswith("http://") or link_url.startswith("https://"):
            all_links.append({"file": file_path, "url": link_url, "type": "external"})
        elif not link_url.startswith("mailto:") and not link_url.startswith("#") and not link_url.startswith("{"): # Ignore mailto, anchor links and dynamic links
            all_links.append({"file": file_path, "url": link_url, "type": "internal"})

    # Find Markdown links
    for match in markdown_link_regex.finditer(content):
        link_url = match.group(2)
        if link_url.startswith("http://") or link_url.startswith("https://"):
            all_links.append({"file": file_path, "url": link_url, "type": "external"})
        elif not link_url.startswith("mailto:") and not link_url.startswith("#"): # Ignore mailto and anchor links
             all_links.append({"file": file_path, "url": link_url, "type": "internal"})

    # Find Astro Image components
    for match in astro_image_regex.finditer(content):
        link_url = match.group(1)
        if not link_url.startswith("http://") and not link_url.startswith("https://") and not link_url.startswith("{"):
            all_links.append({"file": file_path, "url": link_url, "type": "internal_image"})
            
    # Find astro:assets Image components
    # For these, the src is often a variable, so we look for imports and variable assignments if direct src is not found
    # This is a simplified version and might need more sophisticated parsing for complex cases
    # We are looking for { src: "/photos/photo1.jpg", ...}
    for img_match in re.finditer(r'src:\s*["\']([^"\']+)["\']', content):
        img_src = img_match.group(1)
        if not img_src.startswith("http://") and not img_src.startswith("https://") and not img_src.startswith("{"):
             all_links.append({"file": file_path, "url": img_src, "type": "internal_image_asset"})


import json
print(json.dumps(all_links))
