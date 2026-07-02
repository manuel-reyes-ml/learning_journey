# Types
gh label create "type: feature"  --description "New functionality"                   || true
gh label create "type: bug"      --description "Defect or incorrect behavior"        || true
gh label create "type: docs"     --description "Documentation updates"               || true
gh label create "type: test"     --description "Tests / pytest coverage"             || true
gh label create "type: refactor" --description "Refactor without behavior change"    || true

# Priority
gh label create "priority: P0"   --description "Urgent / blocking"                   || true
gh label create "priority: P1"   --description "High priority"                       || true
gh label create "priority: P2"   --description "Normal priority"                     || true

# Engines
gh label create "engine: A-reconcile"     --description "Relius ↔ Matrix reconciliation engine" || true
gh label create "engine: B-age"           --description "Age-based tax code engine"            || true
gh label create "engine: C-roth-taxable"  --description "Roth taxable + basis engine"          || true
gh label create "engine: D-ira-rollover"  --description "IRA rollover engine"          || true

# Areas
gh label create "area: config"     --description "Config/schema mappings"            || true
gh label create "area: cleaning"   --description "Cleaning/normalization modules"   || true
gh label create "area: export"     --description "Correction template export"       || true
gh label create "area: notebooks"  --description "Notebooks / walkthroughs"         || true
gh label create "area: data-visualization"  --description "Plot key metrics / KPIs"         || true