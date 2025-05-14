# SignifyTS - Keria Basic Operations

<div class="alert alert-primary">
  <b>🎯 OBJECTIVE</b><hr>
  Introduce basic operations using Signify-ts: creating a client, initializing (booting) an agent, connecting to an agent, and creating an Autonomic Identifier (AID).</li>
    </ul>
    Familiarity with core KERI concepts (AIDs, KELs, digital signatures, witnesses, OOBIs) is assumed.
</div>

## Create a Client and Connect to the Keria Agent

Now that we understand the architecture, let's see how to use the `signify-ts` library to establish a connection with a Keria agent. This process involves three main steps:
1.  Initializing the `signify-ts` library.
2.  Creating a `SignifyClient` instance, which represents your application's connection to a specific Keria agent.
3.  Bootstrapping and connecting the client to the agent, which establishes the Client AID and the delegated Agent AID.



<div class="alert alert-info">
    <b>ℹ️ Note</b><hr>This section assumes that a Keria agent is running and its Boot and Admin interfaces are accessible at the specified URLs. In the context of these notebooks, Keria is pre-configured and running as part of the Docker deployment.
</div>


### Library Initialization

The `signify-ts` library contains components for cryptographic operations using libsodium. Before any of its functionalities can be used, these components must be initialized. This is achieved by calling and the `ready()` function.



```typescript
import { randomPasscode, ready, SignifyClient, Tier } from 'npm:signify-ts';

await ready();

console.log("Signify-ts library initialized and ready.");
```

    Signify-ts library initialized and ready.


### Creating a SignifyClient Instance
Once the library is initialized, you can create an instance of `SignifyClient`. This object will be your primary interface for all interactions with the Keria agent. It requires several parameters:

- **url**: The URL of the Keria agent's Admin Interface. The client uses this for most command and control operations after the initial connection is established.
- **bran**: A 21-character, high-entropy string, often referred to as a "passcode." This bran serves as the root salt for deriving the Client AID's signing and rotation keys via a Hierarchical Deterministic (HD) key algorithm. It is critical to treat the bran as securely as a private key. Losing it means losing control of the Client AID.
- **tier**: The security tier for the passcode hashing algorithm. Tier.low, Tier.med, and Tier.high represent different computational costs for deriving keys from the bran. Higher tiers are more resistant to brute-force attacks but require more processing power and time.
- **bootUrl**: The URL of the Keria agent's Boot Interface. This is used for the initial setup and provisioning of the agent worker for this client.


```typescript
const adminUrl = 'http://keria:3901'; // Keria agent's Admin Interface URL
const bootUrl = 'http://keria:3903';  // Keria agent's Boot Interface URL

// Generate a new random 21-character bran (passcode/salt)
// In a real application, you would securely store and reuse this bran.
const bran = randomPasscode();

// Create the SignifyClient instance
const client = new SignifyClient(
    adminUrl,
    bran,
    Tier.low, // Using Tier.low for faster execution
    bootUrl
);

console.log('SignifyClient instance created.');
console.log('Using Passcode (bran):', bran);
```

    SignifyClient instance created.
    Using Passcode (bran): CcRRqj0TePDA55SABx2RC


<div class="alert alert-info">
  <b>ℹ️ NOTE</b><hr>
In a production environment, the <code>bran</code> must be securely generated and stored. For a given Client AID, you must consistently use the same bran to reconnect and derive the correct keys. Using <code>randomPasscode()</code> each time, as in this demo, will result in a new Client AID being created or an inability to connect to an existing one if the Keria agent already has a state associated with a different bran for its controller.
</div>

### Bootstrapping and Connecting to the Agent
With the `SignifyClient` instance created, the next step is to establish the initial connection and state with the Keria agent. This involves two methods:

- **`client.boot()`**: Initiates the bootstrapping process with the Keria agent's Boot Interface:
  - The client generates its Client AID using the provided bran.
  - It sends the Client AID's inception event to the Keria agent's Boot Interface.
  - The Keria agent, upon successful verification, creates a delegated Agent AID and returns its inception event to the client. This step essentially provisions the necessary resources and establishes the delegated relationship on the Keria agent for this specific client.

- **`client.connect()`**: After `boot()` (or if the agent has been previously booted with the same bran), connect() establishes the active session with the Keria agent via its Admin Interface.



```typescript
// Bootstrap the connection with the Keria agent
// This creates the Client AID and requests the Agent AID creation.
await client.boot();
console.log('Client boot process initiated with Keria agent.');

// Establish the active connection and retrieve state
await client.connect();
console.log('Client connected to Keria agent.');

// Retrieve and display the current state
const state = await client.state();
console.log('\nConnection State Details:');
console.log('-------------------------');
console.log('Client AID Prefix: ', state.controller.state.i);
console.log('Client AID Keys:   ', state.controller.state.k);
console.log('Client AID Next Keys Digest: ', state.controller.state.n);
console.log('')
console.log('Agent AID Prefix:   ', state.agent.i);
console.log('Agent AID Type:     ', state.agent.et); // Should be 'dip' for delegated inception
console.log('Agent AID Delegator:', state.agent.di); // Should be the Client AID's prefix

```

    Client boot process initiated with Keria agent.
    Client connected to Keria agent.
    
    Connection State Details:
    -------------------------
    Client AID Prefix:  ENr0SirmygYNXmDWVfA1nIPEuJ8cuuERF3tdrABVygQ0
    Client AID Keys:    [ "DJrMmAvxtxUp87pqmPsm4GplkyHXAhQDP2nt2741BVHQ" ]
    Client AID Next Keys Digest:  [ "EDD26Ke2xcwS5LHEt9VwPyYnJz36BYD0l4c4JBOr_jr2" ]
    
    Agent AID Prefix:    EMXvyic779GNcGhexQLeY2_WC-0uuqOcnnDXRR9iV0MB
    Agent AID Type:      dip
    Agent AID Delegator: ENr0SirmygYNXmDWVfA1nIPEuJ8cuuERF3tdrABVygQ0


**Output Explanation:**

- **Client AID Prefix:** The unique, self-certifying identifier for the client, tied to the bran.
- **Client AID Keys:** The current public signing key(s) for the Client AID.
- **Client AID Next Keys Digest:** The digest (hash) of the public key(s) pre-rotated for the next key rotation of the Client AID.
- **Agent AID Prefix:** The unique identifier for the Keria agent worker associated with your client.
- **Agent AID Type:** dip indicates a "delegated inception" event, signifying that this Agent AID's authority is delegated by another AID.
- **Agent AID Delegator:** This crucial field shows the prefix of the Client AID, confirming that the Agent AID is indeed delegated by your Client AID.

## Reconnecting to an Existing Agent
If the Keria agent has already been booted for a specific `bran` (Client AID), you don't need to call `client.boot()` again when using the same bran. You directly use `client.connect()`. Signify-ts will detect the existing state and reconnect.


```typescript
// Create a new client instance with the SAME bran
const client2 = new SignifyClient(
    adminUrl,
    bran, // Using the same bran as the first client
    Tier.low,
    bootUrl
);
console.log('Second SignifyClient instance created with the same bran.');

// Connect without booting, as the agent state for this bran should already exist
await client2.connect();
console.log('Second client connected to the existing Keria agent.');

const state2 = await client2.state();
console.log('\nReconnection State Details:');
console.log('---------------------------');
console.log('Client AID Prefix:  ', state2.controller.state.i); // Should be the same Client AID
console.log('Agent AID Prefix:   ', state2.agent.i);  // Should be the same Agent AID
console.log('Agent AID Delegator:', state2.agent.di); // Should be the same Client AID
```

    Second SignifyClient instance created with the same bran.
    Second client connected to the existing Keria agent.
    
    Reconnection State Details:
    ---------------------------
    Client AID Prefix:   ENr0SirmygYNXmDWVfA1nIPEuJ8cuuERF3tdrABVygQ0
    Agent AID Prefix:    EMXvyic779GNcGhexQLeY2_WC-0uuqOcnnDXRR9iV0MB
    Agent AID Delegator: ENr0SirmygYNXmDWVfA1nIPEuJ8cuuERF3tdrABVygQ0


<div class="alert alert-primary">
<b>📝 SUMMARY</b><hr>
To connect to a Keria agent using Signify-ts:
<ol>
<li>Initialize the library with <code>await ready()</code>.</li>
<li>Create a <code>SignifyClient</code> instance, providing the agent's Admin and Boot URLs, a unique 21-character <code>bran</code> (passcode/salt for key derivation), and a security <code>Tier</code>.</li>
<li>For the first-time connection with a new <code>bran</code>, call <code>await client.boot()</code> to provision the Client AID and request the creation of a delegated Agent AID from Keria.</li>
<li>Call <code>await client.connect()</code> to establish the active session, retrieve the state (Client and Agent AIDs), and complete any delegation approvals. The Client AID delegates authority to the Agent AID, whose inception event (type <code>dip</code>) will list the Client AID as its delegator.</li>
<li>For subsequent connections using the same <code>bran</code>, skip <code>client.boot()</code> and directly use <code>client.connect()</code>.</li>
</ol>
The <code>bran</code> is critical for deriving the Client AID's keys and must be kept secure and reused consistently for the same identity.
</div>

## Add an Autonomic Identifier (AID)

Once your Signify client is connected to the Keria agent, you can instruct the agent to create and manage new Autonomic Identifiers (AIDs) on your behalf. These AIDs will be controlled by your Client AID (established during the `connect()` phase) through the delegation mechanism.

### Initiating AID Inception

Creating a new AID is an asynchronous operation. When you request the Keria agent to incept an AID, the agent starts the process, which might involve communicating with witnesses. The `signify-ts` library handles this by first giving you an "operation" object, which you can then use to poll for the completion of the inception process.

The `client.identifiers().create()` method is used to start the inception of a new AID.

**Parameters Explained:**

- **aidAlias (string):** This is a human-readable alias that you assign to the AID within your Signify client's local storage. It's used to refer to this AID in subsequent client operations. It's not part of the KERI protocol itself but a convenience for client-side management.
- **inceptionArgs (object):** This object contains the configuration for the new AID:
  - **toad (number):** The Threshold of Accountable Duplicity. This is the minimum number of witness receipts the controller (your Client AID via Keria) requires for this new AID's events to be considered accountable.
  - **wits (array of strings):** A list of AID prefixes of the witnesses that this new AID should use. These witnesses must be discoverable by your Keria agent (e.g., pre-loaded during Keria's startup or resolved via OOBIs by the client/agent).
  - **Other parameters:** not shown for brevity but available, see **[CreateIdentifierArgs](https://weboftrust.github.io/signify-ts/interfaces/CreateIdentiferArgs.html)**


```typescript
// Define an alias for the new AID for easy reference within the client
const aidAlias = 'newAid';

// Inception request parameters
const identifierArgs = {
    toad: 3, // Threshold of Accountable Duplicity: minimum number of witness receipts required
    wits: [   // List of witness AID prefixes to use for this AID
        'BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha',
        'BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM',
        'BIKKuvBwpmDVA4Ds-EpL5bt9OqPzWPja2LigFYZN2YfX'
    ]
    // Other parameters can be specified. If not, defaults are used.
};

// Send the inception request to the Keria agent
const inceptionResult = await client.identifiers().create(aidAlias, identifierArgs);
console.log(`AID inception initiated for alias: ${aidAlias}`);

// The result contains information about the long-running operation
const inceptionOperation = await inceptionResult.op();
console.log('Inception Operation Details:');
console.log(inceptionOperation);

```

    AID inception initiated for alias: newAid
    Inception Operation Details:
    {
      name: "witness.EBKArnSgsnEh3Pd5JAk0ctVNaPrjtfX_N27Xz3MttmgX",
      metadata: { pre: "EBKArnSgsnEh3Pd5JAk0ctVNaPrjtfX_N27Xz3MttmgX", sn: 0 },
      done: false,
      error: null,
      response: null
    }


**Outout explained**

Calling `inceptionResult.op()` returns a promise that resolves to an operation object containing:
- **name:** A unique name for this long-running operation (e.g., `witness.AID_PREFIX`). Keria uses this to track the task. The prefix in the name corresponds to the AID being created.
- **metadata:** Contains details like the prefix (pre) of the AID being incepted and the sequence number (`sn`, which is 0 for inception).
- **done:** A boolean indicating if the operation has completed. Initially, it's `false`.
- **error:** Will contain error details if the operation fails.
- **response:** Will contain the result of the operation (the signed inception event) once `done` is `true`.

### Waiting for Operation Completion
Since AID inception involves network communication (e.g., with witnesses to gather receipts), it doesn't complete instantly. You need to poll or wait for the operation to finish. The `client.operations().wait()` method handles this, periodically checking with the Keria agent until the operation's `done` flag becomes `true` or a timeout occurs.


```typescript
// Poll the Keria agent for the completion of the inception operation.
// AbortSignal.timeout(30000) sets a 30-second timeout for waiting.
console.log('Waiting for inception operation to complete...');
const operationResponse = await client
    .operations()
    .wait(inceptionOperation, AbortSignal.timeout(30000)); // Pass the operation name

console.log('\nInception Operation Completed:');
console.log(operationResponse);

// The actual inception event is in the 'response' field of the completed operation
const newAidInceptionEvent = operationResponse.response;
console.log(`\nSuccessfully created AID with prefix: ${newAidInceptionEvent.i}`);
console.log(`Witnesses specified: ${JSON.stringify(newAidInceptionEvent.b)}`);

```

    Waiting for inception operation to complete...
    
    Inception Operation Completed:
    {
      name: "witness.EBKArnSgsnEh3Pd5JAk0ctVNaPrjtfX_N27Xz3MttmgX",
      metadata: { pre: "EBKArnSgsnEh3Pd5JAk0ctVNaPrjtfX_N27Xz3MttmgX", sn: 0 },
      done: true,
      error: null,
      response: {
        v: "KERI10JSON0001b7_",
        t: "icp",
        d: "EBKArnSgsnEh3Pd5JAk0ctVNaPrjtfX_N27Xz3MttmgX",
        i: "EBKArnSgsnEh3Pd5JAk0ctVNaPrjtfX_N27Xz3MttmgX",
        s: "0",
        kt: "1",
        k: [ "DKJtw7dBxxp2MfJo5TLqH3AK8hChBMBuGyPvSd1fT3zE" ],
        nt: "1",
        n: [ "EG2z1Vsli6k0weJOk8ul_e1KaiQRZrvsFe-VBdPL1gGD" ],
        bt: "3",
        b: [
          "BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha",
          "BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM",
          "BIKKuvBwpmDVA4Ds-EpL5bt9OqPzWPja2LigFYZN2YfX"
        ],
        c: [],
        a: []
      }
    }
    
    Successfully created AID with prefix: EBKArnSgsnEh3Pd5JAk0ctVNaPrjtfX_N27Xz3MttmgX
    Witnesses specified: ["BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha","BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM","BIKKuvBwpmDVA4Ds-EpL5bt9OqPzWPja2LigFYZN2YfX"]


**Completed Operation Output Explained:**

- `done`: Now true, indicating the inception is complete on the Keria agent's side.
- `response`: This field now contains the actual signed inception event (`icp`) for the newly created AID (`newAid`).
- `i`: The prefix of the newly created AID.
- `k`: The list of current public signing keys.
- `n`: The list of digests of the next (pre-rotated) public keys.
- `b`: The list of witness AIDs that this AID is configured to use.
- `bt`: The Threshold of Accountable Duplicity (TOAD) specified during creation (matches toad: 2 from our request).

The Keria agent has successfully incepted the AID, and its KEL (starting with this inception event) is now managed by the agent and anchored with the specified witnesses.

## Managing Operations
Signify-ts also provides methods to list and delete operations tracked by the Keria agent for your client.

### List Operations


```typescript
// List all current long-running operations for this client
const operationsList = await client.operations().list();
console.log('\nCurrent Operations List:');
console.log(JSON.stringify(operationsList, null, 2));
```

    
    Current Operations List:
    [
      {
        "name": "witness.EBKArnSgsnEh3Pd5JAk0ctVNaPrjtfX_N27Xz3MttmgX",
        "metadata": {
          "pre": "EBKArnSgsnEh3Pd5JAk0ctVNaPrjtfX_N27Xz3MttmgX",
          "sn": 0
        },
        "done": true,
        "error": null,
        "response": {
          "v": "KERI10JSON0001b7_",
          "t": "icp",
          "d": "EBKArnSgsnEh3Pd5JAk0ctVNaPrjtfX_N27Xz3MttmgX",
          "i": "EBKArnSgsnEh3Pd5JAk0ctVNaPrjtfX_N27Xz3MttmgX",
          "s": "0",
          "kt": "1",
          "k": [
            "DKJtw7dBxxp2MfJo5TLqH3AK8hChBMBuGyPvSd1fT3zE"
          ],
          "nt": "1",
          "n": [
            "EG2z1Vsli6k0weJOk8ul_e1KaiQRZrvsFe-VBdPL1gGD"
          ],
          "bt": "3",
          "b": [
            "BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha",
            "BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM",
            "BIKKuvBwpmDVA4Ds-EpL5bt9OqPzWPja2LigFYZN2YfX"
          ],
          "c": [],
          "a": []
        }
      }
    ]


### Delete Operations


```typescript
// Delete the completed inception operation (optional cleanup)
const opNameToDelete = operationsList[0].name;
await client.operations().delete(opNameToDelete);
console.log(`\nDeleted operation: ${opNameToDelete}`);
```

    
    Deleted operation: witness.EBKArnSgsnEh3Pd5JAk0ctVNaPrjtfX_N27Xz3MttmgX


<div class="alert alert-primary">
<b>📝 SUMMARY</b><hr>
To create a new AID using Signify-ts and a Keria agent:
<ol>
<li>Use <code>client.identifiers().create(alias, config)</code>. Provide a client-side <code>alias</code> for the AID and a <code>config</code> object specifying parameters like <code>toad</code> (Threshold of Accountable Duplicity) and <code>wits</code> (list of witness AIDs).</li>
<li>The <code>create()</code> method returns an object from which you can get a long-running <code>operation</code> object using <code>.op()</code>. This operation is initially marked as not <code>done</code>.</li>
<li>Use <code>client.operations().wait(operationName)</code> to poll the Keria agent until the operation completes. The resolved object will have
<code>done: true</code> and its <code>response</code> field will contain the signed inception event (<code>icp</code>) of the newly created AID.</li>
<li>Operations can be listed with <code>client.operations().list()</code> and deleted with <code>client.operations().delete(operationName)</code>.</li>
</ol>
This process highlights the asynchronous nature of Keria operations that involve agent-side processing and network interactions.
</div>


```typescript

```
