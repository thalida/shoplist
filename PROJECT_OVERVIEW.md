# Project Overview


## Tasks

1. ~~Setup auth / login~~
2. Setup websockets (channels)
3. Setup graphql
4. setup homepage
- show all lists:
  - name
  - description
  - num items remaining (% complete?)
  - last updated


## Components Needed:
-[] Filterable sortable table


## Nav & Routes
- lists:
  - purpose: view all lists
  - pinned lists (action: view all | view list)
  - recent lists (action: view all | view list)
  - all lists table (action: view list)
    - features: search, filter, sort all fields
    - ordered by: last updated
    - name
    - num items remaining (% complete?)
    - last updated
    - category

- products:
  - purpose: view all products
  - all products table (action: view product)
    - features: search, filter, sort all fields
    - ordered by: name
    - name
    - num lists
    - num stores
    - category

- stores:
  - purpose: view all stores
  - all stores table (action: view store)
    - features: search, filter, sort all fields
    - ordered by: name
    - name
    - num lists
    - num products
    - category

- account:
  - purpose: view account settings
  - account settings
    - name
    - email
    - password
  - logout


- list detail view:
  - purpose: view list
  - name
  - description
  - num items remaining (% complete?)
  - last updated
  - products
    - action: groupby category/aisle
    - action: show checked items (always at bottom of section)
    - name
    - quantity needed
    - units
    - aisle

- product detail view:
  - purpose: view product
  - name
  - description
  - lists
    - name
  - stores
    - name

- store detail view:
  - purpose: view store
  - name
  - description
  - lists
    - name
  - products
    - name
    - quantity needed
    - units
