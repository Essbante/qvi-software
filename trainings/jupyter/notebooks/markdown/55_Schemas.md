# ACDC Schemas

<div class="alert alert-primary">
  <b>🎯 OBJECTIVE</b><hr>
    Explain the role of schemas in defining ACDC structures, how they leverage Self-Addressing Identifiers (SAIDs) for verifiability, and learn how to create and process a basic schema.
</div>

## What is a Schema?

Before we can issue or verify an Authentic Chained Data Container, we need a blueprint that describes exactly what information it should contain and how that information should be structured. This blueprint is called a **Schema**.

Schemas serve several purposes:

* **Structure & Validation:** They define the names, data types, and constraints for the data within an ACDC. This allows recipients to validate that a received ACDC contains the expected information in the correct format.
* **Interoperability:** When different parties agree on a common schema, they can reliably exchange and understand ACDCs for a specific purpose (e.g., everyone knows what fields to expect in a "Membership Card" ACDC).
* **Verifiability:** As we'll see, ACDC schemas themselves are cryptographically verifiable, ensuring the blueprint hasn't been tampered with.

## Writing ACDC Schemas

ACDC schemas are written using the **JSON Schema** specification. If you're familiar with JSON Schema, you'll find ACDC schemas very similar, with a few KERI-specific conventions.

Let's look at the main parts of a typical ACDC schema:

```json
{
    "$id": "",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Sample Credential",
    "description": "A very basic credential schema for demonstration.",
    "type": "object",
    "credentialType": "SampleCredential",
    "version": "1.0.0",
    "properties": {
        "v": {
            "description": "Credential Version String",
            "type": "string"
        },
        "d": {
            "description": "Credential SAID",
            "type": "string"
        },
        "u": {
            "description": "One time use nonce",
            "type": "string"
        },
        "i": {
            "description": "Issuer AID",
            "type": "string"
        },
        "rd": {
            "description": "Registry SAID",
            "type": "string"
        },
        "s": {
            "description": "Schema SAID",
            "type": "string"
        },
        "a": {
            "oneOf": [
                {
                    "description": "Attributes block SAID",
                    "type": "string"
                },
                {
                    "$id": "",
                    "description": "Attributes block",
                    "type": "object",
                    "properties": {
                        "d": {
                            "description": "Attributes data SAID",
                            "type": "string"
                        },
                        "i": {
                            "description": "Issuee AID",
                            "type": "string"
                        },
                        "dt": {
                            "description": "Issuance date time",
                            "type": "string",
                            "format": "date-time"
                        },
                        "claim": {
                            "description": "Custom claim being made",
                            "type": "string"
                        }
                    },
                    ...
                }
            ]
        }
    },
    ...
}
```

1.  **Schema Metadata (Top Level):** Describes the schema itself.
    * `$id`: This field holds the SAID of the entire schema file once processed. It's not a URL like in standard JSON Schema. It's computed after all internal SAIDs are calculated.
    * `$schema`: Specifies the JSON Schema version (e.g., `"http://json-schema.org/draft-07/schema#"`)
    * `title`, `description`: Human-readable name and explanation
    * `type`: Usually `"object"` for the top level of an ACDC schema
    * `credentialType`: A specific name for this type of credential
    * `version`: A semantic version for this specific credential type (e.g., `"1.0.0"`) to manage schema evolution (Distinct from the ACDC instance's `v` field).
2.  **`properties` (Top Level):** Defines the fields that will appear in the ACDC's envelope and payload.
    * ACDC Metadata Fields: Defines required fields like
        * `v`: ACDC version/serialization
        * `d`: ACDC SAID
        * `u`: salty nonce
        * `i`: Issuer AID
        * `rd`: Registry SAID
        * `s`: Schema SAID
    * Payload Sections: Defines the payload structures
        * `a`: Defines the structure for the **attributes block**, which holds the actual data or claims being made by the credential.
            * **`oneOf`**: This standard JSON Schema keyword indicates that the value for the `a` block in an actual ACDC instance can be *one of* the following two formats:
                1.  **Compact Form (String):**
                    * `{"description": "Attributes block SAID", "type": "string"}`: This option defines the *compact* representation. Instead of including the full attributes object, the ACDC can simply contain a single string value: the SAID of the attributes block itself. This SAID acts as a verifiable reference to the full attribute data, which might be stored elsewhere. (We won't cover compact ACDCs in this material.)
                2.  **Un-compact Form (Object):**
                    * `{"$id": "", "description": "Attributes block", "type": "object", ...}`: This option defines the full or un-compacted representation, where the ACDC includes the complete attributes object directly.
                        * **`$id`**: This field will hold the SAID calculated for *this specific attributes block structure* after the schema is processed (`SAIDified`). Initially empty `""` when writing the schema.
                        * **`description`**: Human-readable description of this block.
                        * **`type`: `"object"`**: Specifies that this form is a JSON object.
                        * **`properties`**: Defines the fields contained within the attributes object:
                            * **`d`**: Holds the SAID calculated from the *actual data* within the attributes block
                            * **`i`**: The AID of the **Issuee** or subject of the credential – the entity the claims are *about*.
                            * **`dt`**: An ISO 8601 date-time string indicating when the credential was issued.
                            * **`claim`** (and other custom fields): These are the specific data fields defined by your schema. In this example, `"claim"` is a string representing the custom information this credential conveys. You would define all your specific credential attributes here.
3.  **`additionalProperties`, `required`:** Standard JSON Schema fields controlling whether extra properties are allowed and which defined properties must be present. (see the complete schema [here](config/schemas/sample_schema.json.bak))

To write your schema, most of the customization will happen inside the payload attributes block (`a`). Here you can add claims according to specific needs.


<div class="alert alert-info">
  <b>ℹ️ NOTE</b><hr>
    The ACDC schema definitionn allows for optional payload blocks called <code>e</code> (edges) and <code>r</code> (rules).
    <ul>
        <li>The <code>e</code> section defines links (edges) to other ACDCs, creating verifiable chains of related credentials. For more details see <a href="https://trustoverip.github.io/tswg-acdc-specification/#edge-section"><b>edges</b></a></li>
        <li>The <code>r</code> section allows embedding machine-readable rules or legal prose, such as Ricardian Contracts, directly into the credential. For more details see <a href="https://trustoverip.github.io/tswg-acdc-specification/#rules-section"><b>rules</b></a></li>
</div>

<div class="alert alert-primary">
  <b>📝 SUMMARY</b><hr>
An ACDC Schema acts as a verifiable blueprint defining the structure, data types, and rules for an Authentic Chained Data Container (ACDC). Written using the JSON Schema specification, they ensure ACDCs have the expected format (validation) and enable different parties to understand exchanged credentials (interoperability). Key components include top-level metadata (like the schema's SAID in $id, title, credentialType, version) and a properties section defining the ACDC envelope fields (v, d, i, s, etc.) and payload sections. The main payload section is attributes (a), containing issuer/issuee info and custom claims, with optional sections for edges (e) linking other ACDCs and rules (r).
</div>
