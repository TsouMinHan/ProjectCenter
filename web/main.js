
let vm = new Vue({
    el: "#app",
    data: {
        "title": "",
        "project": ""
    },
    mounted: async function set_data(){
        const data = await eel.get_data()();
    
        this.title = data["title"];
        this.project = data["project"];
    },
    methods: {
        run_script: async function(event) {
            const id = event.currentTarget.id;
            const file = event.currentTarget.textContent.trim();
            const venv = document.getElementById(id).getAttribute("name");
            const project_name = id.split("-")[0];
            const script_running_status = await eel.run_script(project_name, file, venv)();
            // alert(script_running_status);
            if (script_running_status == true){
                document.getElementById(id).classList.add('btn-danger');
                document.getElementById(id).classList.remove('btn-primary');
            }
            else if (script_running_status == false){
                document.getElementById(id).classList.add('btn-primary');
                document.getElementById(id).classList.remove('btn-danger');
            }

        }
    }
})

eel.expose(show_message);
function show_message(msg) {
    alert(msg);
}