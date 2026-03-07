// SPDX-FileCopyrightText: 2026 PlainLicense
//
// SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import cloudflareAdapter from '@astrojs/cloudflare';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import favicons from 'astro-favicons';
import starlightContextualMenu from 'starlight-contextual-menu';
import starlightLlmsText from 'starlight-llms-txt';
import starlightScrollToTop from 'starlight-scroll-to-top';

// https://astro.build/config
export default defineConfig({
	site: 'https://readscore.plainlicense.org',
	base: '/',
	adapter: cloudflareAdapter({
		imageService: 'compile',
		// @ts-ignore
		environment: process.env.NODE_ENV === 'development' ? 'local' : undefined,
	}),
	integrations: [
		starlight({
			title: 'readscore',
			logo: {
				src: './src/assets/images/logo_only_color_transp.svg',
				alt: 'PlainLicense Logo'
			},
			description: 'A Python library for calculating readability metrics.',
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/plainlicense/readscore' }
			],
			customCss: [
				'./src/styles/custom.css',
			],
			sidebar: [
				{
					label: 'Getting Started',
					items: [
						{ label: 'Introduction', slug: 'index' },
						{ label: 'Extending readscore', slug: 'guides/extending' },
					],
				},
				{
					label: 'Readability Metrics',
					items: [
						{ label: 'Overview', slug: 'metrics' },
						{ label: 'Choosing a Metric', slug: 'choosing-a-metric' },
						{ label: 'ARI', slug: 'metrics/ari' },
						{ label: 'Coleman-Liau', slug: 'metrics/coleman-liau' },
						{ label: 'Dale-Chall', slug: 'metrics/dale-chall' },
						{ label: 'Flesch Reading Ease', slug: 'metrics/flesch' },
						{ label: 'Flesch-Kincaid', slug: 'metrics/flesch-kincaid' },
						{ label: 'Gunning Fog', slug: 'metrics/gunning-fog' },
						{ label: 'Linsear Write', slug: 'metrics/linsear-write' },
						{ label: 'SMOG', slug: 'metrics/smog' },
						{ label: 'Spache', slug: 'metrics/spache' },
					],
				},
				{
					label: 'Reference',
					autogenerate: { directory: 'reference' },
				},
			],
			plugins: [starlightScrollToTop(), starlightContextualMenu({
				actions: ["copy", "view", "claude", "chatgpt"]
			}),
			// We need to configure starlight-tags with a tags.yml.
			//starlightTags(), 
			starlightLlmsText({
				projectName: "readscore by PlainLicense",
				description: `readscore is a Python library for calculating readability metrics. It provides a simple and efficient way to assess the readability of text using various established metrics.
				`,
				promote: ["index", "metrics/index", "choosing-a-metric"],
				minify: {
					whitespace: true,
					note: true,
					details: true,
				}
			})],
		}),
		mdx(),
		sitemap({
			filter: (page) => !/\^\/(?!cdn-cgi\/)/.test(page),
			namespaces: {
				image: false,
				video: false,
			}
		}),
		favicons({
			name: 'readscore by PlainLicense',
			short_name: 'readscore',
		})
	],
	prefetch: {
		defaultStrategy: "viewport",
	},
	experimental: {
		chromeDevtoolsWorkspace: true,
		clientPrerender: true,
		contentIntellisense: true,
		svgo: {
			plugins: [
				{
					name: "preset-default",
					params: {
					},
				},
			],
		},
		headingIdCompat: true,
		preserveScriptOrder: true,
	},
	output: "static",
	image: {
		service: {
			entrypoint: "astro/assets/services/sharp",
		},
		responsiveStyles: true,
		layout: "constrained",
		domains: ["github.com", "raw.githubusercontent.com", "plainlicense.org"],
	},
	// @ts-ignore
	build: {
		inlineStylesheets: "auto",
		assets: "_astro",
		// @ts-ignore
		cssCodeSplit: true,
		cssMinify: "lightningcss",

		rollupOptions: {
			output: {
				experimentalMinChunkSize: 10000,
			},
		},
	},
	markdown: {
		shikiConfig: { theme: "github-dark" },
	},
	vite: {
		"environments": {
			"ssr": {
				"resolve": {
					"external": [
						"sharp",
						"node:os",
						"node:path",
						"node:child_process",
						"node:crypto",
						"node:tty",
						"node:util"
					]
				}
			}
		},
		plugins: [],
	},
	assetsInclude: [
		"src/*.webp",
		"src/*.png",
		"src/*.jpg",
		"src/*.jpeg",
		"src/*.svg",
		"src/*.avif",
	],
	css: {
		lightningcss: {},
	}
});
