// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://docs.plainlicense.org',
	base: '/readable',
	integrations: [
		starlight({
			title: 'Readable',
			logo: {
				src: './src/assets/images/logo_only_color_transp.svg',
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/plainlicense/readable' }
			],
			customCss: [
				'./src/styles/custom.css',
			],
			sidebar: [
				{
					label: 'Getting Started',
					items: [
						{ label: 'Introduction', slug: 'index' },
						{ label: 'Extending Readable', slug: 'guides/extending' },
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
		}),
	],
});
