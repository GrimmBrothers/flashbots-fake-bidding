pragma solidity >=0.8.15;


contract flasbhot_bug{

    bool variable = true;
    address owner;
    uint256[2] probability;
    uint256 public etherValueMin = 0.0015 ether;
    uint256 public etherValueMax = 0.003 ether;
    address address_1;
    address address_2;

    constructor(uint32 _m, uint32 _n){
        probability[0] = _m;
        probability[1] = _n;
        owner = msg.sender;
    }
    function setProbability(uint32 _m, uint32 _n) public {
        probability[0] = _m;
        probability[1] = _n;
    }
    function changePayments(uint32 _m, uint32 _n) public {
        etherValueMin = _m;
        etherValueMax = _n;
    }

    function setAddress1(address _address) public {
        address_1 = _address;
    }

    function setAddress2(address _address) public {
        address_2 = _address;
    }

    function random() public payable{
        uint256 randomSeed;
        uint256 blockNum = block.number;
        bytes32 blockHash = blockhash(blockNum);
        address blockCoinbase = block.coinbase;
        randomSeed = uint(keccak256(abi.encodePacked(blockHash,blockCoinbase,block.timestamp)));
        if (variable){
            makeOperation(100);
            if(randomSeed%probability[0]<probability[1]){
                block.coinbase.transfer(etherValueMax);
            }
            variable = false;
        }
        else{
            address addr1 = address(bytes20(sha256(abi.encodePacked(msg.sender,block.timestamp))));
            setAddress1(addr1);
            revert();
        }
    }
    function notRandom() public payable {
        if (variable){
            makeOperation(30);
            block.coinbase.transfer(etherValueMin);
            variable = false;
        }
        else{
            address addr = address(bytes20(sha256(abi.encodePacked(msg.sender,block.timestamp))));
            setAddress2(addr);
            revert();
        }
    }
    function changeVariable() public{
        variable = true;
    }
    receive() external payable {} // Required for contract to receive ETH
    fallback() external payable {}
    
    function withdraw() public {
        require(msg.sender == owner);
        payable(owner).transfer(address(this).balance);
    }

    function makeOperation(uint k) pure internal{
        uint256 j;
        for(uint i=0;i<k;i++){
            j = j*i;
        }
    }

}