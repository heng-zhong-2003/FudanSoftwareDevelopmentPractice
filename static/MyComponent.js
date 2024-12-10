const MyComponent = {
    template: `<div> Hello from MyComponent! </div>`
};

const app1= {
  template:`
  <a class="navbar-brand" v-bind:href="index"> $[ message ]</a>
  `,
  data(){
    return{
      message:"Home",
      index:'http://127.0.0.1:5000/pj',
    };
  },
  delimiters: ['$[', ']']
};

const app2= {
  template:`
  <li class="nav-item active">
    <a class="nav-link" v-bind:href="about">About
      <span class="sr-only">(current)</span>
    </a>
  </li>
  `,
  data(){
    return{
      about:'http://127.0.0.1:5000/pj/about',
    };
  },
};

const app3= {
  template:`
    <a class="nav-link" v-bind:href="create">Create</a>
  `,
  data(){
    return{
      create:'http://127.0.0.1:5000/pj/create',
    };
  },
};

const app4= {
  template:`
    <a class="nav-link" v-bind:href="my_related_projects">my_related_projects</a>
  `,
  data(){
    return{
      my_related_projects:'http://127.0.0.1:5000/pj/my_related_projects',
    };
  },
};

const Header_1 = {
    template: `
<nav class="navbar navbar-expand-lg navbar-light bg-primary">
  <div id=app1>
    <app1></app1>
  </div>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
<div class="collapse navbar-collapse" id="navbarNavDropdown">
  <ul class="navbar-nav">
    <li class="nav-item">
      <div id=app2>
        <app2></app2>
      </div>
    </li>
    <li class="nav-item">
      <div id=app3>
        <app3></app3>
      </div>
    </li>
    <li class="nav-item">
      <div id=app4>
        <app4></app4>
      </div>
    </li>
    <li class="nav-item dropdown">
      <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
        Dropdown link
      </a>
      <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
        <a class="dropdown-item" href="#">Action</a>
        <a class="dropdown-item" href="#">Another action</a>
        <a class="dropdown-item" href="#">Something else here</a>
      </div>
    </li>
  </ul>
</div>
</nav>
  `,
  components:{
    app1,app2,app3,app4
  }
};

