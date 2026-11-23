export function transactionState(tx) {
  const phase = String(tx.statusName ?? tx.status_name ?? tx.status ?? 'PENDING').toUpperCase();
  const receipts = tx.consensus_data?.leader_receipt;
  const execution = Array.isArray(receipts) ? receipts.at(-1)?.execution_result : receipts?.execution_result;
  if (/UNDETERMINED|CANCEL|REJECT|FAIL/.test(phase)) return {phase, terminal:true, success:false, detail:execution || 'No successful finalized state change'};
  if (phase === 'FINALIZED') return {phase,terminal:true,success:execution === 'SUCCESS' && tx.result_name === 'MAJORITY_AGREE',detail:execution || tx.result_name || 'Execution unverified'};
  return {phase,terminal:false,success:false,detail:execution || 'Waiting for network consensus'};
}
export async function connectBrowser(provider, chain) {
  if (!provider?.request) throw Error('No browser wallet detected. Choose Prepare in Studio and sign with its built-in wallet.');
  const chainId='0x'+chain.id.toString(16);
  if ((await provider.request({method:'eth_chainId'})).toLowerCase() !== chainId) {
    try { await provider.request({method:'wallet_switchEthereumChain',params:[{chainId}]}); }
    catch (e) {
      if(e.code!==4902) throw e;
      await provider.request({method:'wallet_addEthereumChain',params:[{chainId,chainName:chain.name,nativeCurrency:chain.nativeCurrency,rpcUrls:chain.rpcUrls.default.http}]});
      await provider.request({method:'wallet_switchEthereumChain',params:[{chainId}]});
    }
  }
  const accounts=await provider.request({method:'eth_requestAccounts'});
  if(!accounts?.[0])throw Error('Wallet returned no account.');
  return accounts[0];
}
