# Table of Contents
## 101 Basics KLI
1. [Welcome to vLEI Training - 101](101_05_Welcome_to_vLEI_Training_-_101.md#Welcome-to-vLEI-Training---101)
    1. [Prerequisites](101_05_Welcome_to_vLEI_Training_-_101.md#Prerequisites)
    1. [Versions](101_05_Welcome_to_vLEI_Training_-_101.md#Versions)
1. [Introduction to KERI, ACDC, and vLEI](101_07_Introduction_to-KERI_ACDC_and_vLEI.md#Introduction-to-KERI-ACDC-and-vLEI)
    1. [The KERI Protocol](101_07_Introduction_to-KERI_ACDC_and_vLEI.md#The-KERI-Protocol)
    1. [The ACDC Protocol](101_07_Introduction_to-KERI_ACDC_and_vLEI.md#The-ACDC-Protocol)
    1. [GLEIF vLEI Ecosystem](101_07_Introduction_to-KERI_ACDC_and_vLEI.md#GLEIF-vLEI-Ecosystem)
1. [KERI Command Line Interface](101_10_KERI_Command_Line_Interface.md#KERI-Command-Line-Interface)
    1. [How to use KLI in Notebooks?](101_10_KERI_Command_Line_Interface.md#How-to-use-KLI-in-Notebooks)
    1. [Basic Utility Commands](101_10_KERI_Command_Line_Interface.md#Basic-Utility-Commands)
1. [Controllers and Identifiers](101_15_Controllers_and_Identifiers.md#Controllers-and-Identifiers)
    1. [What is an Identifier?](101_15_Controllers_and_Identifiers.md#What-is-an-Identifier)
    1. [What is a Controller?](101_15_Controllers_and_Identifiers.md#What-is-a-Controller)
    1. [The Key Event Log](101_15_Controllers_and_Identifiers.md#The-Key-Event-Log)
    1. [Advanced Forms of Control](101_15_Controllers_and_Identifiers.md#Advanced-Forms-of-Control)
1. [Working with Keystores and AIDs via KLI](101_20_Working_with_Keystores_and_AIDs_via_KLI.md#Working-with-Keystores-and-AIDs-via-KLI)
    1. [Initializing a Keystore](101_20_Working_with_Keystores_and_AIDs_via_KLI.md#Initializing-a-Keystore)
    1. [Creating an Identifier](101_20_Working_with_Keystores_and_AIDs_via_KLI.md#Creating-an-Identifier)
    1. [The Prefix](101_20_Working_with_Keystores_and_AIDs_via_KLI.md#The-Prefix)
    1. [Displaying the Identifier](101_20_Working_with_Keystores_and_AIDs_via_KLI.md#Displaying-the-Identifier)
    1. [Displaying the KEL](101_20_Working_with_Keystores_and_AIDs_via_KLI.md#Displaying-the-KEL)
    1. [Displaying the keystore Identifiers](101_20_Working_with_Keystores_and_AIDs_via_KLI.md#Displaying-the-keystore-Identifiers)
1. [Signatures](101_25_Signatures.md#Signatures)
    1. [What is a Digital Signature?](101_25_Signatures.md#What-is-a-Digital-Signature)
    1. [Signatures and Verification](101_25_Signatures.md#Signatures-and-Verification)
    1. [Signing and Verifying with KLI](101_25_Signatures.md#Signing-and-Verifying-with-KLI)
1. [Key Rotation and Pre-rotation](101_30_Key_Rotation.md#Key-Rotation-and-Pre-rotation)
    1. [Why is Key Rotation Important?](101_30_Key_Rotation.md#Why-is-Key-Rotation-Important)
    1. [Establishment Events](101_30_Key_Rotation.md#Establishment-Events)
    1. [Pre-Rotation](101_30_Key_Rotation.md#Pre-Rotation)
    1. [Key rotation with KLI](101_30_Key_Rotation.md#Key-rotation-with-KLI)
1. [Modes, OOBIs, and Witnesses](101_35_Modes_oobis_and_witnesses.md#Modes-OOBIs-and-Witnesses)
    1. [Direct and Indirect Modes](101_35_Modes_oobis_and_witnesses.md#Direct-and-Indirect-Modes)
    1. [Out-of-Band Introductions](101_35_Modes_oobis_and_witnesses.md#Out-of-Band-Introductions)
    1. [Witnesses](101_35_Modes_oobis_and_witnesses.md#Witnesses)
    1. [Threshold of Accountable Duplicity](101_35_Modes_oobis_and_witnesses.md#Threshold-of-Accountable-Duplicity)
1. [Witnesses](101_40_Witnesses.md#Witnesses)
    1. [Witness network](101_40_Witnesses.md#Witness-network)
    1. [Initializing a keystore](101_40_Witnesses.md#Initializing-a-keystore)
    1. [Listing keystore contacts](101_40_Witnesses.md#Listing-keystore-contacts)
    1. [Creating an AID](101_40_Witnesses.md#Creating-an-AID)
1. [Connecting controllers](101_45_Connecting_controllers.md#Connecting-controllers)
    1. [Controllers setup](101_45_Connecting_controllers.md#Controllers-setup)
    1. [OOBI setup](101_45_Connecting_controllers.md#OOBI-setup)
    1. [Challenge-response](101_45_Connecting_controllers.md#Challenge-response)
1. [Introduction to ACDCs](101_50_ACDC.md#Introduction-to-ACDCs)
    1. [What is an ACDC?](101_50_ACDC.md#What-is-an-ACDC)
    1. [Self-Addressing Identifiers](101_50_ACDC.md#Self-Addressing-Identifiers)
    1. [Structure of an ACDC](101_50_ACDC.md#Structure-of-an-ACDC)
    1. [ACDCs Security and Verifiability](101_50_ACDC.md#ACDCs-Security-and-Verifiability)
1. [ACDC Schemas](101_55_Schemas.md#ACDC-Schemas)
    1. [What is a Schema?](101_55_Schemas.md#What-is-a-Schema)
    1. [Writing ACDC Schemas](101_55_Schemas.md#Writing-ACDC-Schemas)
1. [Saidifying](101_60_Saidify_schema.md#Saidifying)
    1. [Schema SAIDs](101_60_Saidify_schema.md#Schema-SAIDs)
    1. [SAIDifying a Schema](101_60_Saidify_schema.md#SAIDifying-a-Schema)
    1. [Caching Schemas](101_60_Saidify_schema.md#Caching-Schemas)
1. [ACDC Issuance](101_65_ACDC_Issuance.md#ACDC-Issuance)
    1. [Setting up Holder and Issuer](101_65_ACDC_Issuance.md#Setting-up-Holder-and-Issuer)
    1. [Schema preparation](101_65_ACDC_Issuance.md#Schema-preparation)
    1. [Prepare and Create Credential](101_65_ACDC_Issuance.md#Prepare-and-Create-Credential)
    1. [IPEX Credential Issuance Flow](101_65_ACDC_Issuance.md#IPEX-Credential-Issuance-Flow)
1. [ACDC Presentation and Rovocation](101_70_ACDC_Presentation_and_Revocation.md#ACDC-Presentation-and-Rovocation)
    1. [IPEX Credential Presentation](101_70_ACDC_Presentation_and_Revocation.md#IPEX-Credential-Presentation)
    1. [Credential Presentation Flow](101_70_ACDC_Presentation_and_Revocation.md#Credential-Presentation-Flow)
    1. [Credential revocation](101_70_ACDC_Presentation_and_Revocation.md#Credential-revocation)
1. [ACDC Edges and Rules](101_75_ACDC_Edges_and_Rules.md#ACDC-Edges-and-Rules)
    1. [Edges, Edge Operators and Rules](101_75_ACDC_Edges_and_Rules.md#Edges-Edge-Operators-and-Rules)
    1. [I2I (Issuer-To-Issuee)](101_75_ACDC_Edges_and_Rules.md#I2I-Issuer-To-Issuee)
    1. [NI2I (Not-Issuer-To-Issuee)](101_75_ACDC_Edges_and_Rules.md#NI2I-Not-Issuer-To-Issuee)
    1. [DI2I (Delegated-Issuer-To-Issuee)](101_75_ACDC_Edges_and_Rules.md#DI2I-Delegated-Issuer-To-Issuee)

## 102 Basics Keria-Signify
1. [SignifyTS - Keria Basics](102_05_Keria_Signify.md#SignifyTS---Keria-Basics)
    1. [Keria/Signify Architecture Overview](102_05_Keria_Signify.md#KeriaSignify-Architecture-Overview)
    1. [Keria Service Endpoint Interfaces](102_05_Keria_Signify.md#Keria-Service-Endpoint-Interfaces)
    1. [End Roles](102_05_Keria_Signify.md#End-Roles)
    1. [Client AID and Agent AID](102_05_Keria_Signify.md#Client-AID-and-Agent-AID)
1. [SignifyTS - Keria Basic Operations](102_10_Keria_Signify_Basic_Operations.md#SignifyTS---Keria-Basic-Operations)
    1. [Create a Client and Connect to the Keria Agent](102_10_Keria_Signify_Basic_Operations.md#Create-a-Client-and-Connect-to-the-Keria-Agent)
    1. [Reconnecting to an Existing Agent](102_10_Keria_Signify_Basic_Operations.md#Reconnecting-to-an-Existing-Agent)
    1. [Add an Autonomic Identifier (AID)](102_10_Keria_Signify_Basic_Operations.md#Add-an-Autonomic-Identifier-AID)
    1. [Managing Operations](102_10_Keria_Signify_Basic_Operations.md#Managing-Operations)
1. [Keria-Signify Connecting Controllers](102_15_Keria_Signify_Connecting_Clients.md#Keria-Signify-Connecting-Controllers)
    1. [Controllers Setup](102_15_Keria_Signify_Connecting_Clients.md#Controllers-Setup)
    1. [End Roles](102_15_Keria_Signify_Connecting_Clients.md#End-Roles)
    1. [OOBI Setup](102_15_Keria_Signify_Connecting_Clients.md#OOBI-Setup)
    1. [Challenge-Response](102_15_Keria_Signify_Connecting_Clients.md#Challenge-Response)


```python

```
