methods {
    function totalSupply() external returns uint256 envfree;
    function mint() external;
    function balanceOf(address) external returns uint256 envfree;
}

invariant totalSupplyIsNotNegative()
    totalSupply() >= 0;

rule minting_mints_one_nft(){
    env e;
    address minter;

    require e.msg.value == 0;
    require e.msg.sender == minter;

    mathint balanceBefore = balanceOf(minter);

    currentContract.mint(e);

    assert to_mathint(balanceOf(minter)) == balanceBefore + 1, "One NFT should be minted";

}

// This is known as a parametric rule, as there is a variable of type "method", which we named `f`
// This means, we call any random function `f` with any random calldata `arg` 
// We can also say which contracts we want to call f on, in this case, we said the nft contract
rule sanity {
    env e;
    calldataarg arg;
    method f;
    f(e, arg);
    satisfy true;
}

// parametric rule example
rule no_change_to_total_supply(method f) {
    uint256 totalSupplyBefore = totalSupply();
    env e;
    calldataarg args;
    f(e, args);
    assert totalSupply() == totalSupplyBefore, "Total supply should not change";
}