# Controllers and Identifiers

<div class="alert alert-prymary">
  <b>🎯 OBJECTIVE</b><hr>
Explain the fundamental KERI concepts of Autonomic Identifiers (AIDs), the Controller entity, and the Key Event Log (KEL).
</div>

Before we dive into creating identifiers and doing operations with the KLI, let's understand two fundamental concepts: **Identifiers** and the **Controller**.

## What is an Identifier?

Identifiers are a generic term; they exist in many forms, but here we are concerned with digital identifiers. In a general sense, an identifier is a name, label, or sequence of characters used to uniquely identify something within a given context. Identifiers are useful to assign claims to something or to locate a resource. Common examples of identifiers are domain names, an email, an ID Number, and so on. 

KERI identifiers are called **Autonomic Identifier (AID)**. They have properties that give them additional capabilities compared to traditional digital identifiers. Here's what makes them different:
- **Provide asymmetric key features:** Beyond being an identifier, AIDs provide signing and verification capabilities via public key
- **Cryptographically Bound Control:** AIDs are linked to one or more cryptographic key pairs (public/private) from their moment of creation; this binding forms the basis of their security and allows the holder of the private key(s) to control the identifier and prove that control through digital signatures.
- **Universally Unique:** Like standard UUIDs, AIDs are designed to be globally unique without needing a central issuing authority, thanks to their cryptographic foundation.  
- **Self-Managed:** Unlike traditional identifiers (like usernames or domain names) that rely on central administrators or registries, an AID is managed directly by its owner(s) — known as the Controller — through cryptographic means (specifically, their private keys). 
- **Self-Certifying:** An AID inherently proves its own authenticity. Its validity stems directly from its cryptographic link to its controlling keys, established at its creation, not from an external authority vouching for it.   
- **Control Over Time:** AIDs are designed for persistent control. The identifier's control history is maintained in a verifiable **key event log (KEL)**, allowing keys to be rotated (changed) securely over time without abandoning the identifier itself, even if old keys are compromised.   
- **Authenticates & Authorizes:** The cryptographic nature of an AID allows its Controller to prove their control (authenticate) directly and grant permissions (authorize actions or access related to the AID) without needing a third-party system.
- **Multi-Signature Control (Multisig):** An AID doesn't have to be controlled by just one Controller. KERI supports configurations where multiple key pairs (held by one or multiple Controllers) are required to authorize actions. This can involve needing a specific number of signatures (e.g., 3 out of 5) or advanced weighted threshold multi-signature schemes.   
- **Secure Key Rotation (Pre-rotation):** When control keys need to be changed (rotated), KERI uses a highly secure "pre-rotation" method. In a rotation event, a secure commitment is made to the next set of keys (hiding the actual public keys using a hash). This means the private keys for the next rotation remain unexposed and secure until they are actually needed, protecting the rotation process itself from being hijacked.   
- **Delegation of Authority:** A Controller of one AID can securely grant specific, often limited or revokable, authority to another AID (a delegate).

Don't worry if these features raise many questions right now. We will explain the 'how' behind them gradually in the sections to come.

## What is a Controller?

In KERI, the Controller is the entity that holds the private cryptographic key(s) associated with an Autonomic Identifier and is therefore responsible for managing it. This possession of the private key(s) is the source of its authority and control over the AID.  

So, a Controller is an entity managing their identifiers. Some scenarios can be:
- An individual managing their own digital identity
- An organization managing its official identifier.
- An autonomous piece of software or device managing its own identifier.
- An autonomous piece of software acting on behalf of someone else.   
- A group managing a shared identifier via multi-signature schemes.

There may be other scenarios that define the Controller; the relevant aspect is that it is an entity with access to the AID private keys and can use them.

While the Controller holds authority over the AID, it relies on software to operate and maintain it. In this training, you’ll be using the KLI as the Controller’s tool for interacting with and managing AIDs.

## The Key Event Log

The Controller's authority isn't just a claim; it's proven using cryptography. Controllers possess the private keys associated with their AID. They use these keys to sign messages and authorize actions. Every significant action taken by a Controller regarding their AID – like creating it (inception), changing its keys (rotation), or other interactions – is recorded as a **Key Event**.

These Key Events are stored sequentially in a **Key Event Log (KEL)**. Think of the KEL as the official history book for an AID. Here are some details about the KEL

* It starts with the AID's "birth certificate" – the **Inception Event**.
* Every subsequent authorized change (like a key rotation) is added as a new entry, cryptographically linked to the previous one.
* Anyone can potentially view the KEL to verify the AID's history and current state, but only the Controller(s) can add new, valid events to it.
* There may be multiple copies of a KEL; they can be distributed across a network of witnesses, a concept we will dive deeper into later.

## Advanced Forms of Control

Control in KERI can be quite nuanced. While the Controller ultimately holds authority, they can sometimes grant specific permissions to others:

* **Signing vs. Rotation Authority**: A Controller might keep the power to change the AID's keys (rotation authority) but allow another entity (a "custodian") to perform more routine actions like signing messages (signing authority).
* **Delegation**: A Controller can grant some level of authority to a completely separate Delegated Identifier. This allows for creating hierarchies and complex organizational structures.

We'll explore these advanced concepts like delegation and multi-sig configurations in later sections.

<div class="alert alert-prymary">
  <b>📝 SUMMARY</b><hr>
<p>Fundamental KERI concepts:</p>
<ul>
    <li><strong>Autonomic Identifiers (AIDs):</strong> These are KERI's unique, self-managed digital identifiers. Unlike traditional IDs, they are cryptographically bound to key pairs from creation, are self-certifying (requiring no central authority), and support features like secure key rotation (pre-rotation), multi-signature control, and delegation.</li>
    <li><strong>Controller:</strong> The entity (person, organization, software) holding the private key(s) for an AID, giving it the authority to manage the identifier and authorize actions.</li>
    <li><strong>Key Event Log (KEL):</strong> The secure, append-only, verifiable history for an AID. It records all significant actions (like creation and key rotations) signed by the Controller, allowing anyone to track the identifier's control provenance.</li>
</ul>
<p>In essence, Controllers use their private keys to manage AIDs, and all authoritative actions are recorded in the KEL.</p>
</div>
