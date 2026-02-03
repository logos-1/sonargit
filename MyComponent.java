import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class MyComponent {
    private final MyService myService;

    @Autowired
    public MyComponent(MyService myService) {
        this.myService = myService;
        // ...
    }

    @Autowired // Noncompliant: Classes should not have more than one @Autowired constructor.
    public MyComponent(MyService myService, Integer i) {
        this.myService = myService;
        // ...
    }

    @Autowired // Noncompliant: Classes should not have more than one @Autowired constructor.
    public MyComponent(MyService myService, Integer i, String s) {
        this.myService = myService;
        // ...
    }
}

interface MyService {
}
