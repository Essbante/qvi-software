# Modes, OOBIs, and Witnesses

<div class="alert alert-primary">
  <b>🎯 OBJECTIVE</b><hr>
Explain KERI's Direct and Indirect modes and the key components enabling Indirect Mode: Out-of-Band Introductions (OOBIs) for discovery, Witnesses for availability and consistency, and the Threshold of Accountable Duplicity (TOAD) for managing accountability.
</div>

## Direct and Indirect Modes
KERI provides a secure way to manage Identifiers and track control using verifiable logs of key events (KEL). How these logs are shared and verified between the controller and someone verifying that identifier leads to two operational modes: Direct and Indirect.


### Direct Mode

Direct Mode is a one-to-one approach, similar to a direct conversation.

The controller shares their Key Event Log directly with a specific validator, who verifies the signatures and checks the cryptographic chain to ensure integrity. The method of sharing the KEL is implementation-dependent.

Trust is based solely on verifying the controller’s own signatures, as the validator directly receives and verifies the KEL.

This mode is an option for interactions where both parties can connect directly, even if only occasionally, and need to be online to exchange new events or updates.  

Although we haven't done any interaction so far, all the things we have done until this point fit within the direct mode approach.

### Indirect Mode

Indirect Mode is the highly-available approach, similar to using a trusted public bulletin board instead of direct messaging.

It’s for scenarios where the controller may be offline or needs to serve many validators at once. Rather than relying on direct communication, it introduces infrastructure to keep the key event log reliably accessible.

Trust extends beyond the controller’s signature, relying on a network of Witnesses that verify, sign, and store events.

This mode is ideal for public identifiers, always-verifiable services, one-to-many interactions, or any situation where the controller can’t be constantly online.

## Out-of-Band Introductions

When an AID controller is operating in indirect mode, you need a way to tell others where they can find information about it, like its Key Event Log (KEL). This is where Out-of-Band Introductions (OOBIs) come in.

**What is an OOBI?**

An OOBI is a **discovery mechanism** used in KERI. Its primary purpose is to link a specific KERI AID  to a network location (a URL or URI) where information about that identifier can potentially be found.

The simplest form of an OOBI pairs an AID with a URL. For example:

`("http://8.8.5.6:8080/oobi", "EaU6JR2nmwyZ-i0d8JZAoTNZH3ULvYAfSVPzhzS6b5CM")`

This OOBI suggests that information related to the AID `EaU6JR2nmwyZ-i0d8JZAoTNZH3ULvYAfSVPzhzS6b5CM` might be available at the service endpoint `http://8.8.5.6:8080/oobi`.

The URL representation will be:

http://8.8.5.6:8080/oobi/EaU6JR2nmwyZ-i0d8JZAoTNZH3ULvYAfSVPzhzS6b5CM

**Key Points**

- OOBIs Facilitate Discovery (Out-of-Band): They use existing internet infrastructure (web servers, QR codes, etc.) to share potential (url, aid) links. This happens outside of KERI's core trust guarantees.
- OOBIs Themselves Are NOT Trusted: Receiving an OOBI does not guarantee the URL-AID link is valid or that the data at the URL is legitimate.
- Trust Requires KERI Verification (In-Band): After using an OOBI URL to retrieve data (like a Key Event Log), you must use KERI's standard cryptographic verification methods (checking signatures, verifying event history) to establish trust.

In short, OOBIs help you find potential information; verification ensures you can trust it.

## Witnesses

Witnesses are entities designated by the controller within their AID key event log, acting much like trusted notaries. Their role is to receive key events directly from the controller, verify the controller’s signature, and check that each event aligns with the historical log they maintain.

Once a witness confirms an event is valid and encounters it for the first time, it generates a receipt by signing the event (Witnesses also have their own AID). The witness then stores both the original event and its receipt, alongside receipts from other witnesses, in a local copy of the KEL known as the **Key Event Receipt Log (KERL)**.

Witnesses play a critical role in ensuring the system’s reliability and integrity. They provide availability by forming a distributed service that validators can query to access the KEL of a given prefix, even if the controller itself is unavailable. Additionally, they help ensure consistency: since honest witnesses only sign the first valid version of an event they observe, it becomes significantly harder for a controller to present conflicting log versions (**duplicity**).

It's important to note that witnesses are software components. For the system to improve security and availability, the witness should be deployed independently, ideally operated by different entities, on different infrastructure, from both the controller and each other.

## Threshold of Accountable Duplicity

A key challenge in maintaining the integrity of an identifier's history is preventing the controller from presenting conflicting versions of events. This situation, known as **duplicity**, occurs if a controller improperly signs two or more different key events purporting to be at the same sequence number in their Key Event Log (KEL) – for example, signing two different rotation events both claiming to be sequence number 3. Such conflicting statements undermine trust in the identifier's true state and control. Reasons for duplicity may be due to malicious intent or operational errors. KERI addresses this partly through the behavior of witnesses (who should only sign the first valid event they see per sequence number) and manages the *accountability* for potential duplicity using a specific threshold.

To quantify the level of agreement needed and manage accountability for potential duplicity, the controller specifies a crucial parameter in their KEL: the **Threshold of Accountable Duplicity (TOAD)**. We have seen this parameter before when calling `kli incept`. The `toad` value represents the minimum number of unique witness receipts the controller considers sufficient to accept accountability for a key event.

By gathering receipts that meet or exceed this controller-defined threshold (`toad`), validators gain assurance that the event history they’re watching is the one the controller stands behind and is broadly agreed upon by the witness network. Crucially, while the `toad` defines the controller's threshold for their accountability, a validator may independently establish its own, often higher, threshold of witness receipts required to accept an event as fully validated according to its trust policy. This threshold mechanism, allowing for distinct controller accountability and validator trust levels, is key to KERI's robust fault tolerance, helping distinguish between minor issues and significant, actionable inconsistencies.

<div class="alert alert-prymary">
  <b>📝 SUMMARY</b><hr>
<p>
    KERI supports two main ways for controllers to share their Key Event Logs (KELs): Direct Mode, where the KEL is shared directly with a validator (suitable for 1-to-1 online interactions), and Indirect Mode, which uses infrastructure for high availability, suitable for offline controllers or 1-to-many interactions. Indirect Mode relies on Witnesses, designated entities that receive, verify, receipt, and store events in Key Event Receipt Logs (KERLs), ensuring availability and consistency. Discovery in Indirect Mode uses Out-of-Band Introductions (OOBIs), which are untrusted links pairing an AID with a potential KEL location that requires separate KERI verification. Controllers set a Threshold of Accountable Duplicity (TOAD), the minimum witness receipts needed for them to be accountable for an event, though validators may set their own higher threshold for trust.
</p>
</div>
