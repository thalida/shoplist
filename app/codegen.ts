import type { CodegenConfig } from '@graphql-codegen/cli'

const config: CodegenConfig = {
  schema: "../api/graphql-schema.json",
  documents: ['src/**/*.vue', 'src/**/*.graphql'],
  generates: {
    './src/api/gql/': {
      preset: 'client',
      config: {
        useTypeImports: true
      }
    }
  }
}
export default config
