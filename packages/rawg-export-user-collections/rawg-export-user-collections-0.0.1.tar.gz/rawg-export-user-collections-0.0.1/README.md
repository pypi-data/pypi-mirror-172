# `rawg_export_user_collections`

Export **public** user's collections from the [RAWG.IO](https://rawg.io/) video game database.

## Installation

```bash
pip install rawg_export_user_collections
```

## Options

```
--user_slug USER_SLUG                User slug from which we get collections.

--export_folder_path EXPORT_FOLDER_PATH  Path where to export the file.
```

## Usage

1. Get user slug from user profile page in [rawg.io](https://rawg.io/):

   ![User profile page](./docs/User%20profile%20page.png)

2. Run command:

   ```bash
   rawg_export_user_collections --user_slug=user_slug --export_folder_path=F:\Backup
   ```

3. Exported json:

   ```json
   {
     "count": 2,
     "collections": [
       {
         "id": 25121,
         "name": "Test collection 2",
         "slug": "test-collection-2-2",
         "url": "https://rawg.io/collections/test-collection-2-2",
         "description": "",
         "games_count": 2,
         "created": "2022-10-17T16:46:55.253839Z",
         "updated": "2022-10-17T16:47:55.254037Z",
         "games": [
           {
             "id": 19369,
             "name": "Call of Duty",
             "slug": "call-of-duty",
             "url": "https://rawg.io/games/call-of-duty",
             "released": "2003-10-29",
             "tba": false,
             "rating": 4.19,
             "updated": "2022-10-16T17:47:34",
             "genres": [
               "Action",
               "Shooter"
             ],
             "platforms": [
               "macOS",
               "PC",
               "Xbox 360",
               "PlayStation 3"
             ]
           },
           {
             "id": 56114,
             "name": "Medal of Honor: Frontline",
             "slug": "medal-of-honor-frontline",
             "url": "https://rawg.io/games/medal-of-honor-frontline",
             "released": "2002-05-28",
             "tba": false,
             "rating": 3.92,
             "updated": "2022-09-17T03:52:26",
             "genres": [
               "Shooter"
             ],
             "platforms": [
               "PlayStation 3",
               "Xbox",
               "GameCube",
               "PlayStation 2"
             ]
           }
         ]
       },
       {
         "id": 25120,
         "name": "Test collection 1",
         "slug": "test-collection-1",
         "url": "https://rawg.io/collections/test-collection-1",
         "description": "",
         "games_count": 3,
         "created": "2022-10-17T16:45:50.825922Z",
         "updated": "2022-10-17T16:46:37.110669Z",
         "games": [
           {
             "id": 5679,
             "name": "The Elder Scrolls V: Skyrim",
             "slug": "the-elder-scrolls-v-skyrim",
             "url": "https://rawg.io/games/the-elder-scrolls-v-skyrim",
             "released": "2011-11-11",
             "tba": false,
             "rating": 4.42,
             "updated": "2022-10-13T10:58:37",
             "genres": [
               "Action",
               "RPG"
             ],
             "platforms": [
               "PC",
               "Nintendo Switch",
               "Xbox 360",
               "PlayStation 3"
             ]
           },
           {
             "id": 3498,
             "name": "Grand Theft Auto V",
             "slug": "grand-theft-auto-v",
             "url": "https://rawg.io/games/grand-theft-auto-v",
             "released": "2013-09-17",
             "tba": false,
             "rating": 4.47,
             "updated": "2022-10-15T12:05:16",
             "genres": [
               "Action",
               "Adventure"
             ],
             "platforms": [
               "PC",
               "Xbox Series S/X",
               "PlayStation 4",
               "PlayStation 3",
               "Xbox 360",
               "Xbox One",
               "PlayStation 5"
             ]
           },
           {
             "id": 10615,
             "name": "System Shock 2",
             "slug": "system-shock-2",
             "url": "https://rawg.io/games/system-shock-2",
             "released": "1999-08-11",
             "tba": false,
             "rating": 4.14,
             "updated": "2022-10-03T11:21:32",
             "genres": [
               "Action",
               "Shooter",
               "RPG"
             ],
             "platforms": [
               "PC",
               "macOS",
               "Linux"
             ]
           }
         ]
       }
     ]
   }
   ```
