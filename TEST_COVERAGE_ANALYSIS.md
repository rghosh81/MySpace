# Test Coverage Analysis

## Summary

| Module | Statements | Missed | Coverage |
|---|---:|---:|---:|
| `models.py` | 94 | 34 | **63.8%** |
| `services.py` | 103 | 51 | **50.5%** |
| `validators.py` | 63 | 39 | **38.1%** |
| `utils.py` | 56 | 56 | **0.0%** |
| **TOTAL** | **316** | **180** | **43.0%** |

**Overall coverage: 43.0% (22 tests passing)**

---

## Detailed Gap Analysis

### 1. `utils.py` — 0% coverage (HIGH PRIORITY)

The entire `utils.py` module has **zero test coverage**. This is the single largest gap in the test suite. The following functions are completely untested:

| Function | Lines | Risk |
|---|---|---|
| `slugify()` | 9–16 | Medium — URL generation bugs cause broken links |
| `truncate()` | 19–22 | Low — simple logic but edge cases matter |
| `time_ago()` | 25–42 | High — date math has many edge cases (singular/plural, boundary values) |
| `generate_hash()` | 45–47 | Low — wrapper around hashlib |
| `paginate()` | 50–64 | High — off-by-one errors in pagination are common and user-facing |
| `extract_mentions()` | 67–69 | Medium — regex correctness |
| `extract_hashtags()` | 72–74 | Medium — regex correctness |
| `mask_email()` | 77–84 | Medium — privacy-sensitive, edge cases with short local parts |

**Recommended tests:**
- `slugify`: special characters, unicode, multiple spaces/hyphens, empty string
- `time_ago`: seconds, minutes, hours, days, months, years boundaries; singular vs plural
- `paginate`: page 1, last page, out-of-range page, empty list, single item, exact page boundary
- `mask_email`: normal email, 1-char local, 2-char local, no @ sign
- `extract_mentions`/`extract_hashtags`: multiple matches, no matches, adjacent to punctuation

### 2. `validators.py` — 38.1% coverage (HIGH PRIORITY)

Only `validate_username` and `validate_email` have partial test coverage. Three validators and one utility function are completely untested:

| Function | Coverage | What's Missing |
|---|---|---|
| `validate_username()` | Partial | Missing: too-long username, invalid characters (starts with digit), valid with underscores |
| `validate_email()` | Partial | Missing: various invalid formats (no domain, double @, special chars) |
| `validate_password()` | **None** | All 6 validation rules untested |
| `validate_post_title()` | **None** | All rules untested |
| `validate_post_content()` | **None** | All rules untested |
| `sanitize_html()` | **None** | No tests for HTML stripping |
| `validate_tag()` | **None** | No tests for tag validation |

**Recommended tests:**
- `validate_password`: test each rule independently (missing uppercase, missing lowercase, missing digit, missing special char, too short, empty, valid)
- `validate_post_title`: empty, too short, too long, valid
- `validate_post_content`: empty, too short, too long, valid
- `sanitize_html`: nested tags, self-closing tags, script tags, normal text without HTML
- `validate_tag`: empty, too long, special characters, valid alphanumeric with spaces/hyphens

### 3. `services.py` — 50.5% coverage (MEDIUM PRIORITY)

**`UserService` gaps (lines 36–55):**
- `delete_user()` — entirely untested. No tests verify that admin-only deletion works or that non-admins are rejected.
- `list_users()` — untested. No tests for filtering by role or active status.
- `search_users()` — untested. No tests for partial match, case insensitivity, or empty results.
- `register()` — missing test for duplicate email registration.

**`PostService` gaps (lines 93–124):**
- `get_posts_by_author()` — untested
- `get_posts_by_tag()` — untested
- `get_popular_posts()` — untested (sorting, threshold)
- `delete_post()` — untested (author delete, moderator delete, unauthorized delete)
- `get_feed()` — untested (pagination, sorting by date)

**`CommentService` (lines 128–169) — entirely untested:**
- `add_comment()` — no tests for happy path or error cases (inactive user, unpublished post, empty content)
- `get_comments_for_post()` — untested
- `delete_comment()` — untested (permission checks)
- `get_comments_by_user()` — untested
- `count_comments_for_post()` — untested

### 4. `models.py` — 63.8% coverage (MEDIUM PRIORITY)

**`User` model gaps:**
- `demote()` — untested (lines 39–47). No tests for demotion path or error when demoting a guest.
- `promote()` admin edge case — no test for attempting to promote an admin (should raise ValueError).
- `activate()` — untested (line 55)
- `update_bio()` — untested (lines 59–61). No test for valid update or the 500-char limit.

**`Post` model gaps:**
- `publish()` with inactive author — untested error path (line 78)
- `publish()` with empty title/content — untested error path (line 80)
- `unpublish()` — untested (line 85)
- `edit()` — untested (lines 89–93)
- `add_tag()` duplicate and max-tag error paths — untested (lines 103, 105, 107)
- `remove_tag()` — untested (lines 112–115)

**`Comment` model gaps:**
- `delete()` (soft-delete) — untested (line 128)
- `can_be_deleted_by()` — untested (lines 132–140). This is **security-relevant** — permission checks should absolutely be tested.

---

## Priority Recommendations

### Immediate (P0) — Security & Correctness

1. **Test `Comment.can_be_deleted_by()`** — This is a permission/authorization check. Bugs here are security vulnerabilities. Test all 4 allowed cases (admin, moderator, comment author, post author) and the denied case.

2. **Test `UserService.delete_user()`** — Admin-only operation. Must verify non-admins cannot delete users.

3. **Test `PostService.delete_post()`** — Role-based access control. Must verify unauthorized users are rejected.

4. **Test `validate_password()`** — Password policy enforcement. Each rule should be tested independently.

### High Priority (P1) — Core Functionality

5. **Test all `utils.py` functions** — This module has 0% coverage. `paginate()` and `time_ago()` are particularly prone to edge-case bugs.

6. **Test `CommentService` entirely** — An entire service class with no coverage. All CRUD operations and permission checks need tests.

7. **Test remaining validators** — `validate_post_title`, `validate_post_content`, `sanitize_html`, `validate_tag` are all untested.

### Medium Priority (P2) — Feature Completeness

8. **Test `PostService.get_feed()`** — Pagination logic with sorting.

9. **Test `PostService.get_popular_posts()`** — Threshold filtering and sort order.

10. **Test `UserService.list_users()` and `search_users()`** — Filtering and search functionality.

11. **Test `User.demote()`** and error paths for `promote()`/`demote()`.

12. **Test `Post.edit()`, `unpublish()`, `remove_tag()`** — Mutation methods on the Post model.

---

## Coverage Target

To reach a reasonable **80% coverage target**, we need approximately **35–40 additional tests** focused on the areas above. A stretch goal of **90%** would require ~50 additional tests including edge cases and error paths.

### Suggested test file structure:
```
tests/
├── test_models.py        (expand: +15 tests for demote, activate, bio, edit, unpublish, tags, comments)
├── test_services.py      (expand: +20 tests for delete, list, search, feed, comments)
├── test_validators.py    (expand: +12 tests for password, title, content, html, tag)
└── test_utils.py         (NEW:    +15 tests for slugify, truncate, time_ago, paginate, mentions, email masking)
```

## How to Run Coverage

```bash
# Run tests with coverage report
python -m pytest tests/ --cov=src/myspace --cov-report=term-missing

# Generate HTML report (open htmlcov/index.html)
python -m pytest tests/ --cov=src/myspace --cov-report=html

# Fail if coverage drops below threshold
python -m pytest tests/ --cov=src/myspace --cov-fail-under=80
```
