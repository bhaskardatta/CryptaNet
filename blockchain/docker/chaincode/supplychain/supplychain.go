package main

import (
	"encoding/json"
	"fmt"
	"strings"
	"time"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SmartContract provides functions for managing supply chain data
type SmartContract struct {
	contractapi.Contract
}

// SupplyChainData represents a supply chain data point with encrypted content
type SupplyChainData struct {
	ID              string    `json:"id"`
	OrganizationID  string    `json:"organizationId"`
	Timestamp       time.Time `json:"timestamp"`
	EncryptedData   string    `json:"encryptedData"`   // Encrypted supply chain data
	DataHash        string    `json:"dataHash"`        // Hash of the original data for integrity verification
	DataType        string    `json:"dataType"`        // Type of supply chain data (e.g., shipment, inventory, production)
	AccessControl   []string  `json:"accessControl"`   // List of organizations that can access this data
	AnomalyDetected bool      `json:"anomalyDetected"` // Flag indicating if an anomaly was detected
	AnomalyScore    float64   `json:"anomalyScore"`    // Score indicating the severity of the anomaly
	Explanation     string    `json:"explanation"`     // Explanation of the anomaly (if detected)
}

// AccessPolicy defines who can access what data
type AccessPolicy struct {
	ID             string    `json:"id"`
	OrganizationID string    `json:"organizationId"` // Organization that owns this policy
	DataTypes      []string  `json:"dataTypes"`      // Types of data this policy applies to
	AllowedOrgs    []string  `json:"allowedOrgs"`    // Organizations allowed to access the data
	CreatedAt      time.Time `json:"createdAt"`
	UpdatedAt      time.Time `json:"updatedAt"`
}

// InitLedger adds a base set of supply chain data to the ledger
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	// No initial data needed
	return nil
}

// CreateSupplyChainData adds a new supply chain data point to the ledger
func (s *SmartContract) CreateSupplyChainData(ctx contractapi.TransactionContextInterface, id, organizationID, encryptedData, dataHash, dataType string, accessControl []string) error {
	// Check if the data already exists
	exists, err := s.SupplyChainDataExists(ctx, id)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("the supply chain data %s already exists", id)
	}

	// Get the identity of the client submitting the transaction
	clientOrgID, err := getClientOrgID(ctx)
	if err != nil {
		return err
	}

	// Verify that the client belongs to the organization they claim to represent
	if clientOrgID != organizationID {
		return fmt.Errorf("client from organization %s cannot create data for organization %s", clientOrgID, organizationID)
	}

	// Create the supply chain data object
	supplyChainData := SupplyChainData{
		ID:              id,
		OrganizationID:  organizationID,
		Timestamp:       time.Now(),
		EncryptedData:   encryptedData,
		DataHash:        dataHash,
		DataType:        dataType,
		AccessControl:   accessControl,
		AnomalyDetected: false,
		AnomalyScore:    0.0,
		Explanation:     "",
	}

	// Convert to JSON
	supplyChainDataJSON, err := json.Marshal(supplyChainData)
	if err != nil {
		return err
	}

	// Put the data on the ledger
	return ctx.GetStub().PutState(id, supplyChainDataJSON)
}

// UpdateAnomalyStatus updates the anomaly status of a supply chain data point
func (s *SmartContract) UpdateAnomalyStatus(ctx contractapi.TransactionContextInterface, id string, anomalyDetected bool, anomalyScore float64, explanation string) error {
	// Get the supply chain data
	supplyChainData, err := s.ReadSupplyChainData(ctx, id)
	if err != nil {
		return err
	}

	// Update the anomaly status
	supplyChainData.AnomalyDetected = anomalyDetected
	supplyChainData.AnomalyScore = anomalyScore
	supplyChainData.Explanation = explanation

	// Convert to JSON
	supplyChainDataJSON, err := json.Marshal(supplyChainData)
	if err != nil {
		return err
	}

	// Put the data back on the ledger
	err = ctx.GetStub().PutState(id, supplyChainDataJSON)
	if err != nil {
		return err
	}

	// Emit an event if an anomaly was detected
	if anomalyDetected {
		eventPayload := fmt.Sprintf("{\"id\":\"%s\",\"organizationId\":\"%s\",\"dataType\":\"%s\",\"anomalyScore\":%f}",
			supplyChainData.ID, supplyChainData.OrganizationID, supplyChainData.DataType, anomalyScore)
		err = ctx.GetStub().SetEvent("AnomalyDetected", []byte(eventPayload))
		if err != nil {
			return err
		}
	}

	return nil
}

// ReadSupplyChainData returns the supply chain data stored in the ledger
func (s *SmartContract) ReadSupplyChainData(ctx contractapi.TransactionContextInterface, id string) (*SupplyChainData, error) {
	// Get the supply chain data from the ledger
	supplyChainDataJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if supplyChainDataJSON == nil {
		return nil, fmt.Errorf("the supply chain data %s does not exist", id)
	}

	// Convert the JSON to a SupplyChainData object
	var supplyChainData SupplyChainData
	err = json.Unmarshal(supplyChainDataJSON, &supplyChainData)
	if err != nil {
		return nil, err
	}

	// Get the identity of the client submitting the transaction
	clientOrgID, err := getClientOrgID(ctx)
	if err != nil {
		return nil, err
	}

	// Check if the client is allowed to access this data
	if clientOrgID != supplyChainData.OrganizationID && !contains(supplyChainData.AccessControl, clientOrgID) {
		return nil, fmt.Errorf("client from organization %s is not authorized to read this data", clientOrgID)
	}

	return &supplyChainData, nil
}

// QuerySupplyChainDataByOrg returns all supply chain data for a specific organization
func (s *SmartContract) QuerySupplyChainDataByOrg(ctx contractapi.TransactionContextInterface, organizationID string) ([]*SupplyChainData, error) {
	// Get the identity of the client submitting the transaction
	clientOrgID, err := getClientOrgID(ctx)
	if err != nil {
		return nil, err
	}

	// Check if the client is allowed to query data for this organization
	if clientOrgID != organizationID {
		return nil, fmt.Errorf("client from organization %s is not authorized to query data for organization %s", clientOrgID, organizationID)
	}

	// Query the ledger for all data belonging to this organization
	queryString := fmt.Sprintf(`{"selector":{"organizationId":"%s"}}`, organizationID)
	resultIterator, err := ctx.GetStub().GetQueryResult(queryString)
	if err != nil {
		return nil, err
	}
	defer resultIterator.Close()

	// Collect the results
	var results []*SupplyChainData
	for resultIterator.HasNext() {
		queryResult, err := resultIterator.Next()
		if err != nil {
			return nil, err
		}

		var supplyChainData SupplyChainData
		err = json.Unmarshal(queryResult.Value, &supplyChainData)
		if err != nil {
			return nil, err
		}

		results = append(results, &supplyChainData)
	}

	return results, nil
}

// QueryAnomalies returns all supply chain data points with detected anomalies
func (s *SmartContract) QueryAnomalies(ctx contractapi.TransactionContextInterface) ([]*SupplyChainData, error) {
	// Query the ledger for all data with anomalies
	queryString := `{"selector":{"anomalyDetected":true}}`
	resultIterator, err := ctx.GetStub().GetQueryResult(queryString)
	if err != nil {
		return nil, err
	}
	defer resultIterator.Close()

	// Get the identity of the client submitting the transaction
	clientOrgID, err := getClientOrgID(ctx)
	if err != nil {
		return nil, err
	}

	// Collect the results, filtering for access control
	var results []*SupplyChainData
	for resultIterator.HasNext() {
		queryResult, err := resultIterator.Next()
		if err != nil {
			return nil, err
		}

		var supplyChainData SupplyChainData
		err = json.Unmarshal(queryResult.Value, &supplyChainData)
		if err != nil {
			return nil, err
		}

		// Check if the client is allowed to access this data
		if clientOrgID == supplyChainData.OrganizationID || contains(supplyChainData.AccessControl, clientOrgID) {
			results = append(results, &supplyChainData)
		}
	}

	return results, nil
}

// CreateAccessPolicy creates a new access policy
func (s *SmartContract) CreateAccessPolicy(ctx contractapi.TransactionContextInterface, id, organizationID string, dataTypes, allowedOrgs []string) error {
	// Check if the policy already exists
	exists, err := s.AccessPolicyExists(ctx, id)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("the access policy %s already exists", id)
	}

	// Get the identity of the client submitting the transaction
	clientOrgID, err := getClientOrgID(ctx)
	if err != nil {
		return err
	}

	// Verify that the client belongs to the organization they claim to represent
	if clientOrgID != organizationID {
		return fmt.Errorf("client from organization %s cannot create policy for organization %s", clientOrgID, organizationID)
	}

	// Create the access policy object
	accessPolicy := AccessPolicy{
		ID:             id,
		OrganizationID: organizationID,
		DataTypes:      dataTypes,
		AllowedOrgs:    allowedOrgs,
		CreatedAt:      time.Now(),
		UpdatedAt:      time.Now(),
	}

	// Convert to JSON
	accessPolicyJSON, err := json.Marshal(accessPolicy)
	if err != nil {
		return err
	}

	// Put the policy on the ledger
	return ctx.GetStub().PutState(fmt.Sprintf("POLICY_%s", id), accessPolicyJSON)
}

// ReadAccessPolicy returns the access policy stored in the ledger
func (s *SmartContract) ReadAccessPolicy(ctx contractapi.TransactionContextInterface, id string) (*AccessPolicy, error) {
	// Get the access policy from the ledger
	accessPolicyJSON, err := ctx.GetStub().GetState(fmt.Sprintf("POLICY_%s", id))
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if accessPolicyJSON == nil {
		return nil, fmt.Errorf("the access policy %s does not exist", id)
	}

	// Convert the JSON to an AccessPolicy object
	var accessPolicy AccessPolicy
	err = json.Unmarshal(accessPolicyJSON, &accessPolicy)
	if err != nil {
		return nil, err
	}

	// Get the identity of the client submitting the transaction
	clientOrgID, err := getClientOrgID(ctx)
	if err != nil {
		return nil, err
	}

	// Check if the client is allowed to read this policy
	if clientOrgID != accessPolicy.OrganizationID && !contains(accessPolicy.AllowedOrgs, clientOrgID) {
		return nil, fmt.Errorf("client from organization %s is not authorized to read this policy", clientOrgID)
	}

	return &accessPolicy, nil
}

// CreateSupplyChainDataSimple adds supply chain data with JSON payload (for testing)
func (s *SmartContract) CreateSupplyChainDataSimple(ctx contractapi.TransactionContextInterface, id, jsonData string) error {
	// Check if the data already exists
	exists, err := s.SupplyChainDataExists(ctx, id)
	if err != nil {
		return fmt.Errorf("failed to check if data exists: %v", err)
	}
	if exists {
		return fmt.Errorf("the supply chain data %s already exists", id)
	}

	// Parse the JSON data
	var dataMap map[string]interface{}
	err = json.Unmarshal([]byte(jsonData), &dataMap)
	if err != nil {
		return fmt.Errorf("failed to parse JSON data: %v", err)
	}

	// Create a simple supply chain data object with the JSON data
	supplyChainData := SupplyChainData{
		ID:              id,
		OrganizationID:  "Org1MSP", // Default organization for testing
		Timestamp:       time.Now(),
		EncryptedData:   jsonData,
		DataHash:        "",
		DataType:        "supply_chain",
		AccessControl:   []string{"Org1MSP", "Org2MSP", "Org3MSP"},
		AnomalyDetected: false,
		AnomalyScore:    0.0,
		Explanation:     "",
	}

	// Convert to JSON
	supplyChainDataJSON, err := json.Marshal(supplyChainData)
	if err != nil {
		return err
	}

	// Put the data on the ledger
	return ctx.GetStub().PutState(id, supplyChainDataJSON)
}

// GetAllSupplyChainData returns all supply chain data (for testing)
func (s *SmartContract) GetAllSupplyChainData(ctx contractapi.TransactionContextInterface) ([]*SupplyChainData, error) {
	// Use rich query with empty selector to get all data
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var supplyChainData []*SupplyChainData
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		// Skip if this is not supply chain data (e.g., access policies)
		if strings.HasPrefix(queryResponse.Key, "POLICY_") {
			continue
		}

		var data SupplyChainData
		err = json.Unmarshal(queryResponse.Value, &data)
		if err != nil {
			continue // Skip malformed data
		}

		supplyChainData = append(supplyChainData, &data)
	}

	return supplyChainData, nil
}

// SupplyChainDataExists returns true if the supply chain data with the given ID exists
func (s *SmartContract) SupplyChainDataExists(ctx contractapi.TransactionContextInterface, id string) (bool, error) {
	supplyChainDataJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return supplyChainDataJSON != nil, nil
}

// AccessPolicyExists returns true if the access policy with the given ID exists
func (s *SmartContract) AccessPolicyExists(ctx contractapi.TransactionContextInterface, id string) (bool, error) {
	accessPolicyJSON, err := ctx.GetStub().GetState(fmt.Sprintf("POLICY_%s", id))
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return accessPolicyJSON != nil, nil
}

// Helper function to get the organization ID of the client submitting the transaction
func getClientOrgID(ctx contractapi.TransactionContextInterface) (string, error) {
	clientOrgID, err := ctx.GetClientIdentity().GetMSPID()
	if err != nil {
		return "", fmt.Errorf("failed to get client organization: %v", err)
	}

	return clientOrgID, nil
}

// Helper function to check if a string is in a slice
func contains(slice []string, item string) bool {
	for _, s := range slice {
		if s == item {
			return true
		}
	}
	return false
}

func main() {
	chaincode, err := contractapi.NewChaincode(&SmartContract{})
	if err != nil {
		fmt.Printf("Error creating supply chain chaincode: %s", err.Error())
		return
	}

	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting supply chain chaincode: %s", err.Error())
	}
}
