# Static Code Analysis Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Weak SHA-1 PIN hash | Security — High | 14 | SHA-1 is not suitable for password/PIN storage. | Use a password-hashing method such as `hashlib.pbkdf2_hmac` with a salt. |
| Unsafe temporary filename | Security — Medium | 60 | `tempfile.mktemp()` can create a race condition. | Use `tempfile.NamedTemporaryFile()` or `tempfile.mkstemp()`. |
| Hardcoded gateway secret | Security — Low | 6 | A secret is stored directly in source code. | Read it from an environment variable; use a demo fallback only if required. |
| Predictable OTP generator | Security — Low | 64 | `random.randint()` is not designed for security tokens. | Use `secrets.randbelow()` or `secrets.randbelow(900000) + 100000`. |
| Mutable default argument | Code quality | 17 | `log=[]` is shared between calls. | Default to `None`, then create a new list inside the function. |
| Naming and formatting violations | Style | 9–79 | Several names use camelCase and spacing is inconsistent. | Use `snake_case` and apply consistent spacing. |
