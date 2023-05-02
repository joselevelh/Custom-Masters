import React from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

function Home() {
  const navigate = useNavigate()
  return (
    <Container className="text-center mt-3">
      <Row>
        <Col>
          <h1>Welcome to Lilas</h1>
          <p className="lead">
            The app that helps you connect with your friends in real life
          </p>
        </Col>
      </Row>
      <Row className="mt-3">
        <Col>
          <p>
            Meaningful connections happen in person, and that's
            what we're all about. Whether you're looking to hang out, play
            sports, explore a new city, or just grab a coffee, our app makes it
            easy to let your friends know where you are and what you're up to.
          </p>
        </Col>
      </Row>
      <Row className="mt-3">
        <Col>
          <p>
            We're inspired by the concept of Digital Minimalism. Using technology
            intentionally, to enhance our lives rather than distract from them.
            That's why we've designed our app to be simple and focused, with no
            unnecessary features or distractions. We want you to use our app
            when you need it, and then put your phone away and enjoy the real
            world.
          </p>
        </Col>
      </Row>
      <Row className="mt-3">
        <Col>
          <p>
            Here's how it works: simply drop a pin with your location and
            activity, and your friends will be able to see where you are and
            join you. Maybe you're at the local park, exploring a new bar, or chilling at a friends house. Whatever
            it is, our app makes it easy to invite your friends to join you,
            without having to explicitly invite individuals or message group chats.
          </p>
        </Col>
      </Row>
      <Row className="mt-3">
        <Col>
          <p>
            We believe that real-life connections are more valuable than
            virtual ones, and we hope Lilas will help you build stronger
            relationships with the people you care about. Sign up now to start
            connecting with your friends in a real and meaningful way.
          </p>
        </Col>
      </Row>
      <Row className="mt-3">
        <Col>
          <Button onClick={handleLoginNav} variant="primary" size="lg">
            Sign Up Now
          </Button>
        </Col>
      </Row>
    </Container>
  );
  function handleLoginNav(){
    navigate("/Sign-up")
  }
}

export default Home;
