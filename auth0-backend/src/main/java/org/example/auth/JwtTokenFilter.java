package org.example.auth;

import com.auth0.jwk.GuavaCachedJwkProvider;
import com.auth0.jwk.Jwk;
import com.auth0.jwk.JwkProvider;
import com.auth0.jwk.UrlJwkProvider;
import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.auth0.jwt.interfaces.JWTVerifier;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.web.authentication.preauth.AbstractPreAuthenticatedProcessingFilter;
import org.springframework.web.server.ResponseStatusException;

import javax.servlet.http.HttpServletRequest;
import java.security.interfaces.RSAPublicKey;
import java.util.Arrays;

import static org.springframework.util.ObjectUtils.isEmpty;

public class JwtTokenFilter extends AbstractPreAuthenticatedProcessingFilter {

    private final String tenantUrl;
    private final JwkProvider jwkProvider;

    public JwtTokenFilter(String tenantUrl) {
        this.tenantUrl = tenantUrl;
        jwkProvider = new GuavaCachedJwkProvider(new UrlJwkProvider(tenantUrl));
    }

    private DecodedJWT validateAndDecodeJwt(String token) {
        try {
            DecodedJWT jwt = JWT.decode(token);
            Jwk jwk = jwkProvider.get(jwt.getKeyId());

            Algorithm algorithm = Algorithm.RSA256((RSAPublicKey) jwk.getPublicKey(), null);

            JWTVerifier verifier = JWT.require(algorithm)
                    .withIssuer(tenantUrl)
                    .build();

            return verifier.verify(token);
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "JWT validation failed");
        }
    }

    @Override
    protected Object getPreAuthenticatedPrincipal(HttpServletRequest request) {
        final String header = request.getHeader(HttpHeaders.AUTHORIZATION);
        if (isEmpty(header) || !header.startsWith("Bearer ")) {
            return null;
        }
        DecodedJWT jwt = validateAndDecodeJwt(header.split(" ")[1].trim());

        return JwtAuth.builder()
                .subject(jwt.getSubject())
                .scopes(Arrays.asList(jwt.getClaim("scope").asString().split(" ")))
                .expiresAt(jwt.getExpiresAt())
                .build();
    }

    @Override
    protected Object getPreAuthenticatedCredentials(HttpServletRequest request) {
        return null;
    }

    @Override
    @Autowired
    public void setAuthenticationManager(AuthenticationManager authenticationManager) {
        super.setAuthenticationManager(authenticationManager);
    }
}
