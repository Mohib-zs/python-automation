output "aks_cluster_name" {
  value = module.my-app-aks.aks_name
}

output "aks_cluster_kubeconfig" {
  value     = module.my-app-aks.kube_config_raw
  sensitive = true
}

output "aks_identity" {
  value = module.my-app-aks.cluster_identity
}

output "kubelet_identity" {
  value = module.my-app-aks.kubelet_identity[0].client_id
}

