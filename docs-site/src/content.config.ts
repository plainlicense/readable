// SPDX-FileCopyrightText: 2026 PlainLicense
//
// SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
	docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
};
