# Non-functional requirement categories

Walk this list per product or per business use case. For each category, ask whether it plausibly applies to this product; if it does and isn't addressed anywhere, that's a gap worth surfacing (log it as an open question if you're not the one who can settle it), not a silent omission.

## 1. Look and Feel
Appearance, style, packaging — how the product should look and feel, distinct from how it behaves.

## 2. Usability and Humanity
- **Ease of use** for the intended frequency of use — note the distinction between **easy-to-use** (optimizes ongoing efficiency for frequent users, can justify an upfront learning cost) and **easy-to-learn** (optimizes first-attempt success for infrequent or public users who get no training). Writing the wrong one produces a fit criterion later that measures the wrong thing.
- Personalization and internationalization
- Learning curve
- Understandability and politeness of language/interaction
- Accessibility
- Convenience

## 3. Performance
- Speed and latency
- Safety-critical behavior
- Precision and accuracy
- Reliability and availability
- Robustness and fault tolerance
- Capacity
- Scalability
- Longevity

## 4. Operational and Environmental
- Physical environment the product runs in
- Wider/ecological environment
- Interfacing with adjacent systems
- Productization
- Release cycle
- Backward compatibility

## 5. Maintainability and Support
- Maintenance turnaround
- Supportability
- Adaptability and portability

## 6. Security
Break this into four independently-specifiable aspects rather than writing one generic "shall be secure" statement:
- **Access** — authorized reachability; denying the unauthorized
- **Privacy** — protection from disclosure, plus retention limits
- **Integrity** — data matches its authoritative source and resists corruption
- **Audit** — operations and data are verifiable after the fact

## 7. Cultural
Market and sociological fit; diversity and inclusion.

## 8. Compliance
Legal requirements; industry or organizational standards.

---

**Capturing a vague-sounding one:** a non-functional requirement that sounds subjective at discovery time ("friendly," "authoritative," "professional look") should still be captured as-is — don't dilute or reject it for vagueness now. The fix for vagueness is a fit criterion, attached later (see the fit-criteria skill), not a better-sounding description now.
