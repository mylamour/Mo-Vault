
# Intro

it was developed by dsprenkels, escaped from side-channels & tamper-resistant attack. You can find source code here: [sss-cli](https://github.com/dsprenkels/sss-cli)

and for the static complie purpose, i add `#[cfg(feature="static")]` this to `combine.rs` & `split.rs`.

1. split.rs

```rust
fn main() {
    #[cfg(feature="static")]
    // If not log level has been set, default to info
    if env::var_os("RUST_LOG") == None {
        env::set_var("RUST_LOG", "secret_share_split=info");
    }
```

2. combine.rs

```rust
    #[cfg(feature="static")]
    // If not log level has been set, default to info
    if env::var_os("RUST_LOG") == None {
        env::set_var("RUST_LOG", "secret_share_combine=info");
    }
```
it works well with static flag.

```Dockerfile

FROM ubuntu:latest
COPY secret-share-combine /usr/bin/secret-share-combine
COPY secret-share-split /usr/bin/secret-share-split
RUN echo "Tyler Durden isn't real." | secret-share-split -n 4 -t 3 >shares.txt
RUN cat shares.txt
RUN head -n 3 shares.txt | secret-share-combine
```

# How to complied it with static link

1. Working with `cross`
it was complied by [cross](https://github.com/rust-embedded/cross)
```bash
RUSTFLAGS="-C target-feature=+crt-static" cross build --target x86_64-unknown-linux-gnu --release
```

2. Working with `cargo`

Select your target platform

* x86_64-unknown-linux-musl
* x86_64-unknown-linux-gnu
* i586-unknown-linux-gnu

```bash
rustup target add x86_64-unknown-linux-gnu
RUSTFLAGS="-C target-feature=+crt-static" cargo build --target=x86_64-unknown-linux-gnu --release
```


# Additional info

```bash
➜  sss git:(main) ✗ md5 secret-share-combine secret-share-split 
MD5 (secret-share-combine) = ea1a66b3ad016ae137d3985b15e357a8
MD5 (secret-share-split) = b03ea131d1241b1177f1473e5fbc8e5e
➜  sss git:(main) ✗ shasum secret-share-combine secret-share-split 
9f7c4e38805be0a49a1bca8a4a4468f3b8744419  secret-share-combine
e5fdb6b4e30003e3f349a425da33bb5eab367966  secret-share-split
```