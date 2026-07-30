# osiris-test

Write Osiris tests in Osiris. Run them with the Python test runner you already
use — there is no runner here to learn.

```clojure
(module app.text_test)
(import-for-syntax osiris_test.core :refer [deftest testing is])
(import osiris_test.core :as t)
(import app.text :refer [step])

^{:doc "step adds one."}
(deftest step-adds-one
  (testing "small values"
    (is (= 2 (step 1)))
    (is (= 6 (step 5)))))
```

`deftest step-adds-one` compiles to `def test_step_adds_one()`, which pytest and
unittest collect by their ordinary naming convention. A failure is an ordinary
`AssertionError`, so no adapter or plugin is involved:

```text
AssertionError: small values
(= 2 (step 1))
  left:  2
  right: 3
```

The description comes from `testing`, the form is the Osiris source you wrote,
and both sides are the values the comparison actually saw — `is` binds them once
before comparing, so the report cannot disagree with the assertion.

## Use

```toml
[project]
dependencies = ["osiris-test"]
```

It has to be a runtime dependency rather than a dev one: the compiler resolves
extension macros through the runtime dependency closure, so a dev-only entry is
invisible to `import-for-syntax`. The package ships no runtime beyond its own
failure formatting.

A test module also needs `(import osiris_test.core :as t)` alongside the
`import-for-syntax`. The macros expand to calls on this module, and those calls
resolve in your module, not in the macro's.

## What is not here yet

`are`, fixtures, and compile-time tests for macros and diagnostics. `is`,
`testing` and `deftest` cover ordinary runtime assertions; the rest is deliberate
scope, not oversight.
