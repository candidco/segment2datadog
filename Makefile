.PHONY: build push run tag

build:
	@docker build --build-arg GIT_SHA=$$(git rev-parse HEAD) -t segment-forwarder . 
run:
	@docker run -p8000:8000 -e SEGMENT_SHARED_SECRET=test segment-forwarder

tag:
	@docker tag segment-forwarder $${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/external-services/segment-forwarder

push:
	@docker push $${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/external-services/segment-forwarder
