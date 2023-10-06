import networkx
import networkx.drawing.nx_agraph

"""
python dependencies.py
cat test.dot | dot -Tpng >out.png && open out.png

networkx.DiGraph tree
networkx.DiGraph no edges
networkx.DiGraph visit each node
networkx cluster
G.add_node("")
G.add_edge("","")
"""

DG = networkx.DiGraph()

DG.add_node("northflier ec2 instance", header=True)
DG.add_node("northflier iam instance profile", header=True)
DG.add_node("northflier iam policy", header=True)

DG.add_edge("upload logs", "northflier iam policy")

DG.add_node("terraform scripts", header=True)

DG.add_node("s3 bucket", aws_resource=True)
DG.add_edge("upload logs", "s3 bucket")

DG.add_edge("upload installer", "s3 bucket")
DG.add_edge("upload installer", "northflier iam policy")

DG.add_edge("northflier iam instance profile", "terraform scripts")

DG.add_edge("northflier ec2 instance", "northflier iam instance profile")

DG.add_edge("dev iteration", "northflier ec2 instance")

DG.add_node("northflier", header=True)

DG.add_node("dev iteration", header=True)
DG.add_edge("dev iteration", "report_uptime.sh.j2")
DG.add_edge("dev iteration", "ripgrep.sh.j2")
DG.add_edge("dev iteration", "customize_env.sh.j2")

DG.add_node("save money", header=True)
DG.add_edge("save money", "schedule_final_shutdown.sh.j2")

DG.add_node("scripts_user.sh.j2", script=True)

DG.add_node("learn cloud-init", header=True)
DG.add_edge("learn cloud-init", "cloudwatch.sh.j2")
DG.add_edge("learn cloud-init", "mytest_per_boot.sh.j2")
DG.add_edge("learn cloud-init", "scripts_user.sh.j2")

DG.add_edge("dev iteration", "bash_history.sh.j2")
DG.add_edge("dev iteration", "upload logs")

DG.add_edge("bash_history.sh.j2", "awscli.sh.j2")

DG.add_node("upload logs", header=True)
DG.add_edge("upload logs", "awscli.sh.j2")
DG.add_edge("upload logs", "gather_logs.sh.j2")

DG.add_node("test installer", header=True)
DG.add_edge("test installer", "containers_test.sh.j2")
DG.add_edge("test installer", "cloudelf.sh.j2")
DG.add_edge("test installer", "dns.sh.j2")

DG.add_node("installer readme", header=True)

DG.add_edge("installer readme", "install docker")

DG.add_edge("dev iteration", "fix dns")
DG.add_edge("installer readme", "install docker")

DG.add_edge("dev iteration", "test installer")

DG.add_node("fix dns", header=True)
DG.add_edge("fix dns", "netplan.sh.j2")

DG.add_node("install docker", header=True)
DG.add_node("docker.sh.j2", script=True)
DG.add_edge("install docker", "docker.sh.j2")

DG.add_node("build lightserver installer", header=True)
DG.add_edge("build lightserver installer", "ansible.sh.j2")
DG.add_edge("build lightserver installer", "lightserver_git_repo_clone.sh.j2")

DG.add_edge("lightserver_git_repo_clone.sh.j2", "install secrets")

DG.add_edge("install secrets", "northflier iam policy")

DG.add_node("containers_test.sh.j2")
DG.add_edge("containers_test.sh.j2", "ansible.sh.j2")
DG.add_edge("containers_test.sh.j2", "lxc.sh.j2")
DG.add_edge("containers_test.sh.j2", "cakepalm.sh.j2")

DG.add_node("customize_env.sh.j2")
DG.add_edge("customize_env.sh.j2", "ansible.sh.j2")

DG.add_node("ansible.sh.j2")
DG.add_edge("ansible.sh.j2", "secrets_ansible_vault_pass.sh.j2")  # hide_secrets: true

DG.add_edge("install secrets", "secrets_ansible_vault_pass.sh.j2")

DG.add_node("secrets_ssh_private_key.sh.j2")  # hide_secrets: true
DG.add_edge("secrets_ssh_private_key.sh.j2", "sops.sh.j2")  # hide_secrets: true

DG.add_node("install secrets", header=True)
DG.add_edge("install secrets", "secrets_fetch.sh.j2")
DG.add_edge("install secrets", "secrets_ssh_private_key.sh.j2")

DG.add_edge("secrets_fetch.sh.j2", "awscli.sh.j2")
DG.add_edge("secrets_fetch.sh.j2", "sops.sh.j2")

DG.add_node("dns.sh.j2", script=True)
DG.add_node("fluentd.sh.j2", script=True)
DG.add_node("golang.sh.j2", script=True)

lst = list(networkx.topological_sort(DG))
for item in lst:
    print(item)

networkx.write_gml(DG, "test.gml")
networkx.nx_agraph.write_dot(DG, "test.dot")

# roots = [v for v, d in DG.in_degree() if d == 0]
# leaves = [v for v, d in DG.out_degree() if d == 0]

# print("roots --------------")
# for item in roots:
#     print(item)

# print("leaves --------------")
# for item in leaves:
#     print(item)


def dostuff():
    false_script_nodes = []
    for node, data in DG.nodes(data=True):
        if "script" in data and data["script"] == False:
            false_script_nodes.append(node)

    print(false_script_nodes)
    DG.remove_nodes_from(false_script_nodes)

    print("---leaves---")
    for item in find_leafnodes(DG):
        print(item)


def dostuff3(G):
    # https://stackoverflow.com/a/62187807/1495086
    print("dostuff3")
    s1 = dict(
        (n, d["script"])
        for n, d in G.nodes().items()
        if ("script" in d and d["script"] == True)
    )
    print(f"Nodes found : {len(s1)} : {s1}")


def dostuff4(G):
    print("dostuff4")
    for node, attr in G.nodes().items():
        if "script" in attr and attr["script"] == True:
            print(node)


def dostuff5(G):
    gc = G.copy()
    for node, dct in G.nodes().items():
        if "script" in dct and dct["script"] == False:
            gc.remove_node(node)

    lst = list(networkx.topological_sort(gc))
    for item in lst:
        print(item)


def dostuff6(G):
    gc = G.copy()
    for node, dct in G.nodes().items():
        if "script" in dct and dct["script"] == False:
            gc.remove_node(node)

    lst = list(networkx.topological_sort(gc))
    for item in lst:
        print(item)


def leaf_nodes(G):
    y = [x for x in G.nodes() if G.out_degree(x) == 0 and G.in_degree(x) == 1]

    for item in sorted(y):
        if ".sh.j2" in item:
            print(item)


def nodes_outgoing(G):
    y = [x for x in G.nodes() if G.out_degree(x) >= 1]

    for item in sorted(y):
        if ".sh.j2" in item:
            print(item)


print("")
print("leaf_nodes")
leaf_nodes(DG)

print("")
print("nodes_outgoing")
nodes_outgoing(DG)

# print("")
# dostuff3(DG)

# print("")
# dostuff4(DG)

# print("")
# print("dostuff5")
# dostuff5(DG)

# print("")
# print("dostuff5")
# dostuff5(DG)
