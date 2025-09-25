//
// Verification for GasBadNftMarketplace contract
//

using GasBadNftMarketplace as gasBadNftMarketplace;
using NftMarketplace as nftMarketplace;

methods {
    function _.safeTransferFrom(address, address, uint256) external => DISPATCHER(true);
    function _.onERC721Received(address, address, uint256, bytes ) external => DISPATCHER(true);

    // View Functions
    function getListing(address,uint256) external returns (INftMarketplace.Listing) envfree;
    function getProceeds(address) external returns (uint256) envfree;
}

ghost mathint listingUpdatesCount{
    init_state axiom listingUpdatesCount == 0;
}
ghost mathint log4Count{
    init_state axiom log4Count == 0;
}

hook Sstore s_listings[KEY address nftAddress][KEY uint256 tokenId].price uint256 price {
    listingUpdatesCount = listingUpdatesCount + 1;
}

hook LOG4(uint offset, uint length, bytes32 t1, bytes32 t2, bytes32 t3, bytes32 t4) uint v {
    log4Count = log4Count + 1;
}

////////////////////////////////
// Rules ///////////////////////
////////////////////////////////

invariant anytime_mapping_updated_emit_event() 
    listingUpdatesCount <= log4Count;


rule calling_any_function_should_result_in_each_contract_having_the_same_state(method f,method f2) {
    require f.selector == f2.selector;
    env e;
    calldataarg args;
    address listingAddr;
    uint256 tokenId;
    address seller;

    require(gasBadNftMarketplace.getProceeds(e, seller) == nftMarketplace.getProceeds(e, seller));
    require(gasBadNftMarketplace.getListing(e, listingAddr, tokenId).price == nftMarketplace.getListing(e, listingAddr, tokenId).price);
    require(gasBadNftMarketplace.getListing(e, listingAddr, tokenId).seller == nftMarketplace.getListing(e, listingAddr, tokenId).seller);

    gasBadNftMarketplace.f(e, args);
    nftMarketplace.f2(e, args);
    
    // They end in the same state
    assert(gasBadNftMarketplace.getListing(e, listingAddr, tokenId).price == nftMarketplace.getListing(e, listingAddr, tokenId).price);
    assert(gasBadNftMarketplace.getListing(e, listingAddr, tokenId).seller == nftMarketplace.getListing(e, listingAddr, tokenId).seller);
    assert(gasBadNftMarketplace.getProceeds(e, seller) == nftMarketplace.getProceeds(e, seller));

}