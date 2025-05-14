# Keria-Signify Connecting Controllers

<div class="alert alert-primary">
  <b>🎯 OBJECTIVE</b><hr>
  Explain how to establish a secure, mutually authenticated connection between two Keria/Signify-ts controllers using Out-of-Band Introductions (OOBIs) and the challenge/response protocol to enhance trust.
</div>

## Controllers Setup

This notebook focuses on connecting two independent controllers using the Keria/Signify architecture. This involves two `SignifyClient` instances, each managing its own AID, establishing contact, and then authenticating each other. Conceptually, these steps mirror the `kli` process for connecting controllers but are executed through the `signify-ts` library interacting with Keria agents.

You will begin by setting up two distinct `SignifyClient` instances, which we'll call `clientA` (representing a controller Alfred) and `clientB` (representing a controller Betty). Each client will:
1.  Generate a unique `bran` (passcode).
2.  Instantiate `SignifyClient`.
3.  Boot and connect to its Keria agent, establishing its Client AID and the delegated Agent AID.
4.  Create a primary AID (let's call them `aidA` for Alfred and `aidB` for Betty) with a set of predefined witnesses.

The specifics of client creation, booting, connecting, and basic AID inception using `signify-ts` were covered in the "Keria-Signify Basic Operations" notebook. You will apply those principles below:



```typescript
import { randomPasscode, ready, SignifyClient, Tier } from 'npm:signify-ts';

const url = 'http://keria:3901';
const bootUrl = 'http://keria:3903';

// Inception request parameters
const identifierArgs = {
    toad: 3,
    wits: [  
        'BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha',
        'BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM',
        'BIKKuvBwpmDVA4Ds-EpL5bt9OqPzWPja2LigFYZN2YfX'
    ]
};

await ready();

// ----- Client A (Alfred) -----

const aidAAlias = 'aidA'
const branA = randomPasscode();
const clientA = new SignifyClient(url, branA, Tier.low, bootUrl);

await clientA.boot();
await clientA.connect();

const AInceptionResult = await clientA.identifiers().create(aidAAlias, identifierArgs);

const AInceptionOperation = await AInceptionResult.op();

const { response: aidA }  = await clientA
    .operations()
    .wait(AInceptionOperation, AbortSignal.timeout(30000));

await clientA.operations().delete(AInceptionOperation.name);

// ----- Client B (Betty) -----

const aidBAlias = 'aidB'
const branB = randomPasscode();
const clientB = new SignifyClient(url, branB, Tier.low, bootUrl);

await clientB.boot();
await clientB.connect();

const BInceptionResult = await clientB.identifiers().create(aidBAlias, identifierArgs);

const BInceptionOperation = await BInceptionResult.op();

const { response: aidB }  = await clientB
    .operations()
    .wait(BInceptionOperation, AbortSignal.timeout(30000));

await clientB.operations().delete(BInceptionOperation.name);

console.log(`Client A AID Pre: ${aidA.i}\nClient B AID Pre: ${aidB.i}`)
```

    Client A AID Pre: EHjjBLJqwM7fuj3e0jBfxYiOi1C5akapvM0rb3iJdAHF
    Client B AID Pre: EGQZYxPrzTuAfijuS0A7UXKgVdaqwcqHBtCEFmCHMmKA


<div class="alert alert-info">
    <b>ℹ️ Note</b><hr> For this demonstration, both clients will connect to the same Keria instance (defined by <code>url</code> and <code>bootUrl</code>). In a real-world scenario, Alfred and Betty would likely each have their own Signify clients running on their respective devices and interacting with their own (or chosen) Keria agent instances. The Keria agent URLs might be different for each. However, the KERI protocol and Signify patterns for connection and authentication remain the same.
</div>

## End Roles

As discussed in "Keria-Signify Basics", when a `SignifyClient` connects, it establishes a **Client AID** (which you directly control via the `bran`) and a delegated **Agent AID** (managed by the Keria service). For these Agent AIDs to act effectively on behalf of the AIDs we just created (`aidA` and `aidB`), we need to explicitly authorize them by assigning an `agent` end role.

The `agent` role, in this context, signifies that the Keria Agent AID associated with `clientA` is authorized to manage/interact on behalf of `aidA`, and similarly for `clientB` and `aidB`. This is a crucial step for enabling the Keria agent to perform tasks like responding to OOBI requests for these specific identifiers.

Use the `client.identifiers().addEndRole()` method to add the role. This method requires:
- The alias of the identifier granting the authorization (e.g., `aidAAlias`).
- The role to be assigned (e.g., `'agent'`).
- The prefix of the AID being authorized for that role. In this case, it's the prefix of the client's own Keria Agent AID, accessible via `client.agent!.pre`.


```typescript
// ----- Client A: Assign 'agent' role for aidA to its Keria Agent AID -----
const agentRole = 'agent';

// Authorize clientA's Agent AID to act as an agent for aidA
const AAddRoleResult = await clientA
    .identifiers()
    .addEndRole(aidAAlias, 
                agentRole, 
                clientA!.agent!.pre // clientA.agent.pre is the Agent AID prefix
               ); 

const AAddRoleOperation = await AAddRoleResult.op();

const { response: AAddRoleResponse } = await clientA
    .operations()
    .wait(AAddRoleOperation, AbortSignal.timeout(30000));

await clientA.operations().delete(AAddRoleOperation.name);

console.log(`Client A: Assigned '${agentRole}' role to Keria Agent ${clientA.agent!.pre} for AID ${aidA.i}`);

// ----- Client B: Assign 'agent' role for aidB to its Keria Agent AID -----

// Authorize clientB's Agent AID to act as an agent for aidB
const BAddRoleResult = await clientB
    .identifiers()
    .addEndRole(aidBAlias, 
                agentRole, 
                clientB!.agent!.pre // clientB.agent.pre is the Agent AID prefix
               ); 

const BAddRoleOperation = await BAddRoleResult.op();

const { response: BAddRoleResponse } = await clientB
    .operations()
    .wait(BAddRoleOperation, AbortSignal.timeout(30000));

await clientB.operations().delete(BAddRoleOperation.name);

console.log(`Client B: Assigned '${agentRole}' role to Keria Agent ${clientB.agent!.pre} for AID ${aidB.i}`);

```

    Client A: Assigned 'agent' role to Keria Agent EP-NHU2XnUC4U5dQjhVWjjr9XRyBvDhtfeUZ_HDmerEn for AID EHjjBLJqwM7fuj3e0jBfxYiOi1C5akapvM0rb3iJdAHF
    Client B: Assigned 'agent' role to Keria Agent ED3KFLOButsKS9sJ8hT2PD061RW0PUohsKimVvo6RwNj for AID EGQZYxPrzTuAfijuS0A7UXKgVdaqwcqHBtCEFmCHMmKA


## OOBI Setup

With the AIDs created and their respective Keria agents authorized, Alfred (`clientA`, `aidA`) and Betty (`clientB`, `aidB`) need a way to discover each other. This is where Out-of-Band Introductions (OOBIs) are used.

### OOBI Exchange

Each client needs to generate an OOBI for its AID (`aidA` and `aidB`). This OOBI is associated with the `agent` role, meaning the OOBI URL (**IURL** for short) will point to an endpoint on their Keria agent that is authorized to serve information about the AID.

Proceed by generating the IURLs:
- `clientA` generates an OOBI for `aidA` with the role `agent`.
- `clientB` generates an OOBI for `aidB` with the role `agent`.



```typescript
// ----- Generate OOBIs -----

// Client A generates OOBI for aidA (role 'agent')
const oobiA_Result = await clientA.oobis().get(aidAAlias, agentRole);
const oobiA_url = oobiA_Result.oobis[0]; // Assuming at least one OOBI is returned
console.log(`Client A (Alfred) generated OOBI for aidA: ${oobiA_url}`);

// Client B generates OOBI for aidB (role 'agent')
const oobiB_Result = await clientB.oobis().get(aidBAlias, agentRole);
const oobiB_url = oobiB_Result.oobis[0]; // Assuming at least one OOBI is returned
console.log(`Client B (Betty) generated OOBI for aidB: ${oobiB_url}`);

```

    Client A (Alfred) generated OOBI for aidA: http://keria:3902/oobi/EHjjBLJqwM7fuj3e0jBfxYiOi1C5akapvM0rb3iJdAHF/agent/EP-NHU2XnUC4U5dQjhVWjjr9XRyBvDhtfeUZ_HDmerEn
    Client B (Betty) generated OOBI for aidB: http://keria:3902/oobi/EGQZYxPrzTuAfijuS0A7UXKgVdaqwcqHBtCEFmCHMmKA/agent/ED3KFLOButsKS9sJ8hT2PD061RW0PUohsKimVvo6RwNj


### OOBI Resolution

In a real scenario, Alfred would share `oobiA` with Betty, and Betty would share `oobiB` with Alfred through some non-KERI channel (e.g., email, QR code, messaging app). For this notebook, we'll just store them in variables.

Now perform the OOBI resolution. This means `clientA`'s Keria agent uses the URL in `oobiB` to fetch `aidB`'s KEL from `clientB`'s Keria agent. `clientA` then cryptographically verifies this KEL. `clientB` resolves `oobiA` similarly.




```typescript
// Client A resolves Client B's OOBI
const contactBAlias = 'Betty_Contact_for_Alfred'; // Alias for clientA to refer to aidB
console.log(`\nClient A (Alfred) attempting to resolve Betty's OOBI...`);
const AResolveOperation = await clientA.oobis().resolve(oobiB_url, contactBAlias);
const AResolveResponse = await clientA
    .operations()
    .wait(AResolveOperation, AbortSignal.timeout(30000));
await clientA.operations().delete(AResolveOperation.name);
console.log(`Client A resolved Betty's OOBI. Response:`, AResolveResponse.response ? "OK" : "Failed or no response data");

// Client B resolves Client A's OOBI
const contactAAlias = 'Alfred_Contact_for_Betty'; // Alias for clientB to refer to aidA
console.log(`\nClient B (Betty) attempting to resolve Alfred's OOBI...`);
const BResolveOperation = await clientB.oobis().resolve(oobiA_url, contactAAlias);
const BResolveResponse = await clientB
    .operations()
    .wait(BResolveOperation, AbortSignal.timeout(30000));
await clientB.operations().delete(BResolveOperation.name);
console.log(`Client B resolved Alfred's OOBI. Response:`, BResolveResponse.response ? "OK" : "Failed or no response data");

```

    
    Client A (Alfred) attempting to resolve Betty's OOBI...
    Client A resolved Betty's OOBI. Response: OK
    
    Client B (Betty) attempting to resolve Alfred's OOBI...
    Client B resolved Alfred's OOBI. Response: OK


### Verify Contacts

Upon successful resolution, each client will have added the other's AID to their local contact list. Use `clientA.contacts().list()` to display the contacts:


```typescript
console.log(`\nVerifying contacts...`);
const AContacts = await clientA.contacts().list(undefined, 'alias', contactBAlias);
console.log(AContacts);

const BContacts = await clientB.contacts().list(undefined, 'alias', contactAAlias);
console.log(BContacts);

```

    
    Verifying contacts...
    [
      {
        alias: "Betty_Contact_for_Alfred",
        oobi: "http://keria:3902/oobi/EGQZYxPrzTuAfijuS0A7UXKgVdaqwcqHBtCEFmCHMmKA/agent/ED3KFLOButsKS9sJ8hT2PD061RW0PUohsKimVvo6RwNj",
        id: "EGQZYxPrzTuAfijuS0A7UXKgVdaqwcqHBtCEFmCHMmKA",
        ends: {
          agent: {
            ED3KFLOButsKS9sJ8hT2PD061RW0PUohsKimVvo6RwNj: { http: "http://keria:3902/" }
          },
          witness: {
            "BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha": {
              http: "http://witness-demo:5642/",
              tcp: "tcp://witness-demo:5632/"
            },
            BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM: {
              http: "http://witness-demo:5643/",
              tcp: "tcp://witness-demo:5633/"
            },
            "BIKKuvBwpmDVA4Ds-EpL5bt9OqPzWPja2LigFYZN2YfX": {
              http: "http://witness-demo:5644/",
              tcp: "tcp://witness-demo:5634/"
            }
          }
        },
        challenges: [],
        wellKnowns: []
      }
    ]
    [
      {
        alias: "Alfred_Contact_for_Betty",
        oobi: "http://keria:3902/oobi/EHjjBLJqwM7fuj3e0jBfxYiOi1C5akapvM0rb3iJdAHF/agent/EP-NHU2XnUC4U5dQjhVWjjr9XRyBvDhtfeUZ_HDmerEn",
        id: "EHjjBLJqwM7fuj3e0jBfxYiOi1C5akapvM0rb3iJdAHF",
        ends: {
          agent: {
            "EP-NHU2XnUC4U5dQjhVWjjr9XRyBvDhtfeUZ_HDmerEn": { http: "http://keria:3902/" }
          },
          witness: {
            "BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha": {
              http: "http://witness-demo:5642/",
              tcp: "tcp://witness-demo:5632/"
            },
            BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM: {
              http: "http://witness-demo:5643/",
              tcp: "tcp://witness-demo:5633/"
            },
            "BIKKuvBwpmDVA4Ds-EpL5bt9OqPzWPja2LigFYZN2YfX": {
              http: "http://witness-demo:5644/",
              tcp: "tcp://witness-demo:5634/"
            }
          }
        },
        challenges: [],
        wellKnowns: []
      }
    ]


## Challenge-Response

Successfully resolving an OOBI means you've retrieved and cryptographically verified the KEL of the target AID. This establishes the authenticity and integrity of the AID's key history.

However, it does not, by itself, prove that the entity you are currently communicating with over the network (the one that provided the OOBI or is responding via the OOBI's endpoint) is the legitimate controller of that AID's private keys.

This is why the **Challenge-Response** protocol is critical for establishing authenticated control.

The process, as described in the "Connecting Controllers" notebook for `kli`, is as follows for each pair (e.g., Alfred challenging Betty):

1.  **Generate Challenge**: Alfred (`clientA`) generates a set of unique challenge words.
2.  **Send Challenge (Simulated OOB)**: Alfred communicates these words to Betty through an out-of-band channel (e.g., verbally, secure message). This step is crucial to prevent a Man-in-the-Middle (MITM) on the main KERI connection from intercepting or altering the challenge. For this notebook, we'll print the words.
3.  **Respond to Challenge**: Betty (`clientB`), using `aidB`, signs the exact challenge words received from Alfred. The `respond()` method sends this signed response to Alfred's Keria agent.
4.  **Verify Response**: Alfred (`clientA`) receives the signed response. His Keria agent verifies that the signature corresponds to `aidB`'s current authoritative keys (from the KEL he resolved earlier) and that the signed message matches the original challenge words. This is an asynchronous operation.
5.  **Mark as Responded/Authenticated**: If verification is successful, Alfred (`clientA`) marks the challenge for `aidB` as successfully responded to and authenticated. This updates the contact information for Betty in Alfred's client.

This process is then repeated with Betty challenging Alfred.

### Generate Challenge Words

Generate a set of random words for each client. `signify-ts` uses `client.challenges().generate()` for this. The strength of the challenge can be specified by the bit length (e.g., 128 or 256 bits, which translates to a certain number of words).


```typescript
// ----- Generate Challenge Words -----

// Client A (Alfred) generates challenge words for Betty
const challengeWordsA = await clientA.challenges().generate(128); // 128-bit strength
console.log("Client A's challenge words for Betty:", challengeWordsA.words);

// Client B (Betty) generates challenge words for Alfred
const challengeWordsB = await clientB.challenges().generate(128); // 128-bit strength
console.log("Client B's challenge words for Alfred:", challengeWordsB.words);
```

    Client A's challenge words for Betty: [
      "tennis",  "boat",
      "bench",   "obscure",
      "chuckle", "raw",
      "salt",    "member",
      "end",     "shock",
      "rebel",   "fall"
    ]
    Client B's challenge words for Alfred: [
      "alpha",   "custom",
      "veteran", "spirit",
      "arch",    "used",
      "benefit", "hybrid",
      "coin",    "pupil",
      "recall",  "foil"
    ]


### Respond and Verify

Perform the following sequence of steps to simulate the challenge/respond protocol.

Assume Alfred has securely (out-of-band) communicated `challengeWordsA.words` to Betty.
- Betty will now use `clientB.challenges().respond()` to sign these words with `aidB` and send the response to `aidA`.
- Alfred will then use `clientA.challenges().verify()` to verify Betty's response. This verification is an operation that needs to be polled.
- Finally, Alfred uses `clientA.challenges().responded()` to mark the contact as authenticated.



```typescript
// ----- Betty (Client B) responds to Alfred's (Client A) challenge -----
console.log(`\nBetty (aidB: ${aidB.i}) responding to Alfred's (aidA: ${aidA.i}) challenge...`);

// Betty uses aidBAlias to sign, targeting aidA.i with challengeWordsA.words
await clientB.challenges().respond(aidBAlias, aidA.i, challengeWordsA.words);
console.log("Betty's response sent.");

// ----- Alfred (Client A) verifies Betty's (Client B) response -----
console.log(`\nAlfred (aidA) verifying Betty's (aidB) response...`);

// Alfred verifies the response allegedly from aidB.i using challengeWordsA.words
const AVerifyBOperation = await clientA.challenges().verify(aidB.i, challengeWordsA.words);

const { response: AVerifyBResponseDetails } = await clientA
    .operations()
    .wait(AVerifyBOperation, AbortSignal.timeout(30000));

await clientA.operations().delete(AVerifyBOperation.name);

const exnSaidB = AVerifyBResponseDetails.exn.d;
console.log("Alfred: Betty's response verified. SAID of exn:", exnSaidB);

// Alfred marks the challenge for Betty (aidB.i) as successfully responded
await clientA.challenges().responded(aidB.i, exnSaidB);
console.log("Alfred: Marked Betty's contact as authenticated.");


// Check Alfred's contact list for Betty's authenticated status
const AContactsAfterAuth = await clientA.contacts().list(undefined, 'alias', contactBAlias);

console.log(AContactsAfterAuth)
```

    
    Betty (aidB: EGQZYxPrzTuAfijuS0A7UXKgVdaqwcqHBtCEFmCHMmKA) responding to Alfred's (aidA: EHjjBLJqwM7fuj3e0jBfxYiOi1C5akapvM0rb3iJdAHF) challenge...
    Betty's response sent.
    
    Alfred (aidA) verifying Betty's (aidB) response...
    Alfred: Betty's response verified. SAID of exn: ENl885g016nPuYhk7ptgj9TVENSPhnbc-g7qBbIZkFqX
    Alfred: Marked Betty's contact as authenticated.
    [
      {
        alias: "Betty_Contact_for_Alfred",
        oobi: "http://keria:3902/oobi/EGQZYxPrzTuAfijuS0A7UXKgVdaqwcqHBtCEFmCHMmKA/agent/ED3KFLOButsKS9sJ8hT2PD061RW0PUohsKimVvo6RwNj",
        id: "EGQZYxPrzTuAfijuS0A7UXKgVdaqwcqHBtCEFmCHMmKA",
        ends: {
          agent: {
            ED3KFLOButsKS9sJ8hT2PD061RW0PUohsKimVvo6RwNj: { http: "http://keria:3902/" }
          },
          witness: {
            "BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha": {
              http: "http://witness-demo:5642/",
              tcp: "tcp://witness-demo:5632/"
            },
            BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM: {
              http: "http://witness-demo:5643/",
              tcp: "tcp://witness-demo:5633/"
            },
            "BIKKuvBwpmDVA4Ds-EpL5bt9OqPzWPja2LigFYZN2YfX": {
              http: "http://witness-demo:5644/",
              tcp: "tcp://witness-demo:5634/"
            }
          }
        },
        challenges: [
          {
            dt: "2025-05-13T20:32:22.631000+00:00",
            words: [
              "tennis",  "boat",
              "bench",   "obscure",
              "chuckle", "raw",
              "salt",    "member",
              "end",     "shock",
              "rebel",   "fall"
            ],
            said: "ENl885g016nPuYhk7ptgj9TVENSPhnbc-g7qBbIZkFqX",
            authenticated: true
          }
        ],
        wellKnowns: []
      }
    ]


Now, the roles reverse. Assume Betty (Client B) has securely (out-of-band) communicated `challengeWordsB.words` to Alfred (Client A).
Alfred will use `clientA.challenges().respond()` to sign these words with `aidA` and send the response to `aidB`.
Betty will then use `clientB.challenges().verify()` to verify Alfred's response and `clientB.challenges().responded()` to mark the contact.


```typescript
// ----- Alfred (Client A) responds to Betty's (Client B) challenge -----
console.log(`\nAlfred (aidA: ${aidA.i}) responding to Betty's (aidB: ${aidB.i}) challenge...`);

// Alfred uses aidAAlias to sign, targeting aidB.i with challengeWordsB.words
await clientA.challenges().respond(aidAAlias, aidB.i, challengeWordsB.words);
console.log("Alfred's response sent.");

// ----- Betty (Client B) verifies Alfred's (Client A) response -----
console.log(`\nBetty (aidB) verifying Alfred's (aidA) response...`);

// Betty verifies the response allegedly from aidA.i using challengeWordsB.words
const BVerifyAOperation = await clientB.challenges().verify(aidA.i, challengeWordsB.words);

const { response: BVerifyAResponseDetails } = await clientB
    .operations()
    .wait(BVerifyAOperation, AbortSignal.timeout(30000));

await clientB.operations().delete(BVerifyAOperation.name);


const exnSaidA = BVerifyAResponseDetails.exn.d;
console.log("Betty: Alfred's response verified. SAID of exn:", exnSaidA);

// Betty marks the challenge for Alfred (aidA.i) as successfully responded
await clientB.challenges().responded(aidA.i, exnSaidA);

console.log("Betty: Marked Alfred's contact as authenticated.");


// Check Betty's contact list for Alfred's authenticated status
const BContactsAfterAuth = await clientB.contacts().list(undefined, 'alias', contactAAlias);

console.log(BContactsAfterAuth);
```

    
    Alfred (aidA: EHjjBLJqwM7fuj3e0jBfxYiOi1C5akapvM0rb3iJdAHF) responding to Betty's (aidB: EGQZYxPrzTuAfijuS0A7UXKgVdaqwcqHBtCEFmCHMmKA) challenge...
    Alfred's response sent.
    
    Betty (aidB) verifying Alfred's (aidA) response...
    Betty: Alfred's response verified. SAID of exn: EAoMCfmMmeJ45t_D4I4aqGWnscNIa82zgkzhYwcyRd3H
    Betty: Marked Alfred's contact as authenticated.
    [
      {
        alias: "Alfred_Contact_for_Betty",
        oobi: "http://keria:3902/oobi/EHjjBLJqwM7fuj3e0jBfxYiOi1C5akapvM0rb3iJdAHF/agent/EP-NHU2XnUC4U5dQjhVWjjr9XRyBvDhtfeUZ_HDmerEn",
        id: "EHjjBLJqwM7fuj3e0jBfxYiOi1C5akapvM0rb3iJdAHF",
        ends: {
          agent: {
            "EP-NHU2XnUC4U5dQjhVWjjr9XRyBvDhtfeUZ_HDmerEn": { http: "http://keria:3902/" }
          },
          witness: {
            "BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha": {
              http: "http://witness-demo:5642/",
              tcp: "tcp://witness-demo:5632/"
            },
            BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM: {
              http: "http://witness-demo:5643/",
              tcp: "tcp://witness-demo:5633/"
            },
            "BIKKuvBwpmDVA4Ds-EpL5bt9OqPzWPja2LigFYZN2YfX": {
              http: "http://witness-demo:5644/",
              tcp: "tcp://witness-demo:5634/"
            }
          }
        },
        challenges: [
          {
            dt: "2025-05-13T20:32:23.131000+00:00",
            words: [
              "alpha",   "custom",
              "veteran", "spirit",
              "arch",    "used",
              "benefit", "hybrid",
              "coin",    "pupil",
              "recall",  "foil"
            ],
            said: "EAoMCfmMmeJ45t_D4I4aqGWnscNIa82zgkzhYwcyRd3H",
            authenticated: true
          }
        ],
        wellKnowns: []
      }
    ]


If both challenge-response cycles complete successfully, Alfred and Betty have now established a mutually authenticated connection. This provides a strong foundation of trust for subsequent interactions, such as exchanging verifiable credentials.


<div class="alert alert-primary">
<b>📝 SUMMARY</b><hr>
This notebook demonstrated the process of connecting two Keria/Signify controllers, Alfred (<code>clientA</code>) and Betty (<code>clientB</code>):
<ol>
    <li><b>Initial Setup:</b> Each client was initialized, booted its Keria agent, connected, and created an Autonomic Identifier(<code>aidA</code> for Alfred, <code>aidB</code> for Betty).</li>
    <li><b>End Role Assignment:</b> The Keria Agent AID for each client was authorized with an <code>agent</code> end role for its respective AID (<code>aidA</code> and <code>aidB</code>). This allows the Keria agent to manage these AIDs, such as serving their KELs via OOBIs. This was done using <code>client.identifiers().addEndRole()</code>.</li>
    <li><b>OOBI Generation & Resolution:</b>
        <ul>
            <li>Each client generated an OOBI URL for its AID, specifically for the <code>'agent'</code> role, using <code>client.oobis().get(alias, 'agent')</code>. This OOBI points to their Keria agent's endpoint for that AID.</li>
            <li>The OOBIs were (simulated) exchanged out-of-band.</li>
            <li>Each client then resolved the other's OOBI using <code>client.oobis().resolve()</code>. This retrieved and cryptographically verified the other's KEL, adding them to their local contact list.</li>
        </ul>
    </li>
    <li><b>Challenge-Response Protocol for Mutual Authentication:</b>
        <ul>
            <li>Each client generated unique challenge words using <code>client.challenges().generate()</code>.</li>
            <li>These words were (conceptually) exchanged out-of-band.</li>
            <li><b>Cycle 1 (Betty responds to Alfred):</b>
                <ul>
                    <li>Betty signed Alfred's challenge words with <code>aidB</code> using <code>clientB.challenges().respond()</code>.</li>
                    <li>Alfred verified Betty's signed response against <code>aidB</code>'s known keys using <code>clientA.challenges().verify()</code>.</li>
                    <li>Upon successful verification, Alfred marked Betty's contact as authenticated using <code>clientA.challenges().responded()</code>.</li>
                </ul>
            </li>
            <li><b>Cycle 2 (Alfred responds to Betty):</b> The same process was repeated with Alfred responding to Betty's challenge.</li>
        </ul>
    </li>
</ol>
Successful completion of both OOBI resolution and the mutual challenge-response protocol establishes a high degree of trust. Both controllers have verified each other's identity (KEL) and cryptographically confirmed that the other party has active control of their private keys. The <code>challengesAuthenticated</code> flag in their contact lists for each other should now be true.
</div>


```typescript

```
