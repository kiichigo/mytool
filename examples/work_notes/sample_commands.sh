#!/usr/bin/env bash
set -euo pipefail

DB=${1:-work_notes.db}
PROFILE=${PROFILE:-examples/work_notes/profile.yaml}

mytool profile-info "$PROFILE"
mytool validate-edge "$PROFILE" person created work

mytool --db "$DB" add-node author_a --kind person --label "Author A"
mytool --db "$DB" add-node composer_b --kind person --label "Composer B"
mytool --db "$DB" add-node studio_c --kind organization --label "Studio C"
mytool --db "$DB" add-node sky_castle --kind work --label "Sky Castle"
mytool --db "$DB" add-node levitation_stone --kind concept --label "Levitation Stone"
mytool --db "$DB" add-node flying_city --kind concept --label "Flying City"

mytool --db "$DB" add-edge author_a created sky_castle
mytool --db "$DB" add-edge composer_b composed_music_for sky_castle
mytool --db "$DB" add-edge studio_c produced sky_castle
mytool --db "$DB" add-edge sky_castle features levitation_stone
mytool --db "$DB" add-edge sky_castle features flying_city
mytool --db "$DB" add-edge levitation_stone related_to flying_city
